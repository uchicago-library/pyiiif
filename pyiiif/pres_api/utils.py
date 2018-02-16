import requests


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
    from . import ImageApiUrl
    if preserve_ratio:
        width = "!"+str(width)
    # If we pass an identifier just try and
    # get the record from the identifier.
    if isinstance(rec, str):
        rec = get_record(rec, request_timeout=request_timeout)
    rec = update_record(rec)
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
