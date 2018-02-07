import re
import urllib.parse
from functools import partial

import requests

from . import ImageApiUrl
from .constants import valid_schemes, valid_image_formats
from .exceptions import ParameterError


def escape_identifier(identifier):
    """
    Escapes a string identifier for inclusion in a URL

    :param str identifier: The identifier to escape
    :rtype: str
    :returns: The identifier, escaped
    """
    return urllib.parse.urlquote(identifier, safe='')


def unescape_identifier(identifier):
    """
    Unescapes a string escaped by :func:`escape_identifier`

    :param str identifier: The escaped identifier
    :rtype: str
    :returns: The identifier, unescaped
    """
    return urllib.parse.urlunquote(identifier)


def update_record(rec, request_timeout=1/10):
    """
    Updates a record from it's URI location

    :param dict/str rec: The record, or a record URI to resolve
    :param int request_timeout: How long to wait for a response for the server
        before raising a :class:`requests.exceptions.Timeout`
    :rtype: dict
    :returns: The record, updated from the URL in its @id
    """
    if isinstance(rec, str):
        rec = get_record(rec, request_timeout=request_timeout)
    # This is a little weird in the instance where the initial
    # input is a string, but in theory I think we make this
    # request again, derived from the record @id, in case the @id
    # in the record we just downloaded is different from what was
    # passed to the function.
    resp = requests.get(rec['@id'])
    resp.raise_for_status()
    updated_rec = resp.json()
    rec.update(updated_rec)
    return rec


def get_record(uri, request_timeout=1/10, update=False):
    """
    Retrieves a record from a URL

    :param str uri: The URL to retrieve the record from
    :param int request_timeout: How long to wait for a response for the server
        before raising a :class:`requests.exceptions.Timeout`
    :param bool update: Whether or not to update the record from it's @id URI
        after retrieving it initially.
    """
    resp = requests.get(uri)
    resp.raise_for_status()
    rj = resp.json()
    if update:
        rj = update_record(rj, request_timeout=request_timeout)
    return rj


def get_hardcoded_thumbnail(rec, width=200, height=200, preserve_ratio=True,
                            request_timeout=1/10, allow_non_iiif=False):
    """
    Retrieves **only** explicitly delineated thumbnails from records

    :param dict/str rec: A record representing an object to retrieve
        a thumbnail for, or the URL at which once can be found.
    :param int width: The requested width of the thumbnail, in pixels
    :param int height: The requested height of the thumbnail, in pixels
    :param bool preserve_ratio: If True, consider width and height to be
        maximum allowable values - but reduce whichever is appropriate to
        maintain the aspect ratio of the returned thumbnail
    :param int request_timeout: How long to wait for a response for the server
        before raising a :class:`requests.exceptions.Timeout`
    :param bool allow_non_iiif: Allow the function to return thumbnails which
        aren't IIIF URLs - this means that if a record hard codes a static
        image link as a thumbnail you'll get that back, even if it isn't below
        the requested width/height
    """
    # If no thumbnail dict bail out
    if isinstance(rec, str):
        rec = get_record(rec, request_timeout=request_timeout, update=True)
    if not rec.get("thumbnail"):
        return None
    if preserve_ratio:
        width = "!"+str(width)
    # If the thumbnail claims the IIIF Image API Service use it
    if rec['thumbnail'].get("service") and \
            rec['thumbnail']['service'].get("@context") in  \
            ["http://iiif.io/api/image/2/context.json"]:
        u = ImageApiUrl.from_url(rec['thumbnail']['@id'])
        u.size = "{},{}".format(width, height)
        return u.to_image_url()
    # Otherwise it's just a link in the @id field
    # Return this only if allowed explicitly
    else:
        if allow_non_iiif:
            if rec['thumbnail'].get("@id"):
                return rec['thumbnail']['@id']


def get_thumbnail(rec, width=200, height=200, preserve_ratio=True,
                  request_timeout=1/10, allow_non_iiif=False):
    """
    Retrieve a thumbnail from any IIIF Presentation API Record

    Retrieves/prefers explicitly specified thumbnails, but will
    recurse through the record tree looking for a asset with a thumbnail
    (or to turn into a thumbnail) otherwise.

    :param dict/str rec: A record representing an object to retrieve
        a thumbnail for, or the URL at which once can be found.
    :param int width: The requested width of the thumbnail, in pixels
    :param int height: The requested height of the thumbnail, in pixels
    :param bool preserve_ratio: If True, consider width and height to be
        maximum allowable values - but reduce whichever is appropriate to
        maintain the aspect ratio of the returned thumbnail
    :param int request_timeout: How long to wait for a response for the server
        before raising a :class:`requests.exceptions.Timeout`
    :param bool allow_non_iiif: Allow the function to return thumbnails which
        aren't IIIF URLs - this means that if a record hard codes a static
        image link as a thumbnail you'll get that back, even if it isn't below
        the requested width/height
    """
    if preserve_ratio:
        width = "!"+str(width)
    # If we pass an identifier just try and
    # get the record from the identifier.
    if isinstance(rec, str):
        rec = get_record(rec, request_timeout=request_timeout, update=True)
    # If one is hardcoded
    hctn = get_hardcoded_thumbnail(
        rec, width=width, height=height,
        preserve_ratio=False, allow_non_iiif=allow_non_iiif
    )
    if hctn:
        return hctn
    # Handy partial - otherwise this turns into an unreadable mess
    # Note we _never_ pass preserve ratio here - if the caller wanted
    # it it's already been handled by the function the operation isn't
    # idempotent
    get_tn = partial(
        get_thumbnail,
        width=width, height=height,
        preserve_ratio=False, request_timeout=request_timeout,
        allow_non_iiif=allow_non_iiif
    )
    # Recurse, depending on record type
    if rec['@type'] == "sc:Collection":
        # prefer the first member, if it exists
        if rec.get("members"):
            return get_tn(rec['members'][0])
        # otherwise try for manifests
        elif rec.get("manifests"):
            return get_tn(rec['manifests'][0])
        # finally check for subcollections
        elif rec.get("collections"):
            return get_tn(rec['collections'][0])
        else:
            return None
    elif rec['@type'] == "sc:Manifest":
        # sequences MUST be > 0
        return get_tn(rec['sequences'][0])
    elif rec['@type'] == "sc:Sequence":
        # canvases MUST be > 0
        return get_tn(rec['canvases'][0])
    elif rec['@type'] == "sc:Canvas":
        if rec.get('images'):
            return get_tn(rec['images'][0])
        else:
            return None
    # We made it!
    elif rec['@type'] == "oa:Annotation":
        # Be sure we haven't stumbled into something
        # that isn't an image
        if rec.get("resource") is None:
            return None
        x = rec['resource']['@id']
        u = ImageApiUrl.from_url(x)
        u.size = "{},{}".format(width, height)
        return u.to_image_url()


def parse_image_api_url_scheme_url_component(url):
    """
    Grabs the 'scheme' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    scheme = urllib.parse.urlparse(url).scheme
    if scheme not in valid_schemes:
        raise ParameterError(
            "Valid schemes include: {}".format(", ".join(valid_schemes))
        )
    return scheme


def parse_image_api_url_server_url_component(url):
    """
    Grabs the 'server' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    return urllib.parse.urlparse(url).netloc


def parse_image_api_url_prefix_url_component(url):
    """
    Grabs the 'prefix' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    if url.endswith("info.json"):
        p = urllib.parse.urlparse(url).path
        if len(p.split("/")) > 3:
            return "/".join(p.split("/")[0:-2])
        return ""
    else:
        p = urllib.parse.urlparse(url).path
        if len(p.split("/")) > 6:
            return "/".join(p.split("/")[0:-5])
        return ""


def parse_image_api_url_identifier_url_component(url):
    """
    Grabs the 'identifier' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    if url.endswith("info.json"):
        p = urllib.parse.urlparse(url).path
        s = p.split("/")[-2]
        return s
    else:
        p = urllib.parse.urlparse(url).path
        s = p.split("/")[-5]
        return s


def parse_image_api_url_region_url_component(url):
    """
    Grabs the 'region' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    # .../full/full/0/default.jpg
    # .../square/full/0/default.jpg
    p = urllib.parse.urlparse(url).path
    s = p.split("/")[-4]
    if s in ("full", "square"):
        return s
    # .../125,15,120,140/full/0/default.jpg
    elif re.match("[0-9]+,[0-9]+,[0-9]+,[0-9]+$", s):
        for x in s.split(","):
            try:
                int(x)
            except ValueError:
                raise ParameterError("Incorrect region parameter")
        return s
    # region=pct:41.6,7.5,40,70
    elif s.startswith("pct:"):
        for x in s[4:].split(","):
            try:
                float(x)
            except ValueError:
                raise ParameterError("Incorrect region parameter")
        return s
    # Error case
    else:
        raise ParameterError("Incorrect region parameter")


def parse_image_api_url_size_url_component(url):
    """
    Grabs the 'size' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    p = urllib.parse.urlparse(url).path
    s = p.split("/")[-3]
    # /full/full/0/default.jpg
    # /full/max/0/default.jpg
    if s in ("full", "max"):
        # Deprecation Warning in the spec about "full"
        return s
    # .../full/150,/0/default.jpg
    elif s.endswith(","):
        try:
            int(s[:-1])
        except ValueError:
            raise ParameterError("Incorrect size parameter")
        return s
    # .../full/,150/0/default.jpg
    elif s.startswith(","):
        try:
            int(s[1:])
        except ValueError:
            raise ParameterError("Incorrect size parameter")
        return s
    # .../full/pct:50/0/default.jpg
    elif s.startswith("pct:"):
        try:
            float(s[4:])
        except ValueError:
            raise ParameterError("Incorrect size parameter")
        return s
    # .../full/225,100/0/default.jpg
    # .../full/!225,100/0/default.jpg
    elif re.match("^(\!)?[0-9]+,[0-9]+$", s):
        if s.startswith("!"):
            c = s[1:]
        else:
            c = s
        for x in c.split(","):
            try:
                int(x)
            except ValueError:
                raise ParameterError("Incorrect size parameter")
        return s
    # Error case
    else:
        raise ParameterError("Incorrect size parameter")


def parse_image_api_url_rotation_url_component(url):
    """
    Grabs the 'roration' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    # .../full/full/0/default.jpg
    # .../full/full/!0/default.jpg
    p = urllib.parse.urlparse(url).path
    s = p.split("/")[-2]
    if s.startswith("!"):
        if len(s) < 2:
            raise ParameterError("Incorrect rotation parameter")
        c = s[1:]
    else:
        c = s
    try:
        assert(0 <= float(c) <= 360)
        return s
    # Error case
    except (ValueError, AssertionError):
        raise ParameterError("Incorrect rotation parameter")


def parse_image_api_url_quality_url_component(url):
    """
    Grabs the 'quality' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    p = urllib.parse.urlparse(url).path
    subp = p.split("/")[-1]
    qual = subp.split(".")[0]
    if qual in ("color", "gray", "bitonal", "default"):
        return qual
    else:
        raise ParameterError("Incorrect quality parameter")


def parse_image_api_url_format_url_component(url):
    """
    Grabs the 'format' component from an IIIF Image API URL

    :param str url: The Image API URL
    :rtype: str
    :returns: The url component
    """
    p = urllib.parse.urlparse(url).path
    fmt = p.split(".")[-1]
    if fmt in valid_image_formats:
        return fmt
    else:
        raise ParameterError("Incorrect format parameter")
