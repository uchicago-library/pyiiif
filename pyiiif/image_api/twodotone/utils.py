import urllib
import re

from ..exceptions import ParameterError
from ..constants import valid_schemes, valid_image_formats


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
