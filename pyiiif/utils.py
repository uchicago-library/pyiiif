from urllib.request import quote, unquote
from pyiiif.constants import valid_contexts

def escape_identifier(identifier):
    """
    Escapes a string identifier for inclusion in a URL

    :param str identifier: The identifier to escape
    :rtype: str
    :returns: The identifier, escaped
    """
    return quote(identifier, safe='')


def unescape_identifier(identifier):
    """
    Unescapes a string escaped by :func:`escape_identifier`

    :param str identifier: The escaped identifier
    :rtype: str
    :returns: The identifier, unescaped
    """
    return unquote(identifier)

def convert_context_url_into_lookup(a_url):
    """tries to look up a IIIF context url in the key value of the valid_contexts dict

    If cannot find the url will return None else will return the right key for defining 
    a context value on a record

    :rtype None or str
    """
    pot_context = a_url
    for key, value in valid_contexts.items():
        if value == pot_context:
            return key
    return None

