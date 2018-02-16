import urllib.parse


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
