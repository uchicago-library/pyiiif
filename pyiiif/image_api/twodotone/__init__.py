from urllib.parse import urlparse
from urllib.parse import quote
from urllib.parse import urlunparse

from .utils import parse_image_api_url_scheme_url_component, \
    parse_image_api_url_server_url_component, \
    parse_image_api_url_prefix_url_component, \
    parse_image_api_url_identifier_url_component, \
    parse_image_api_url_region_url_component, \
    parse_image_api_url_size_url_component, \
    parse_image_api_url_rotation_url_component, \
    parse_image_api_url_quality_url_component, \
    parse_image_api_url_format_url_component
from ...exceptions import ParameterError


# {scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}


class ImageApiUrl:
    """
    A class for parsing, creating, and manipulating IIIF Image API URLs
    """
    @classmethod
    def from_image_url(cls, url):
        """
        Instantiate an instance from an image URL

        :param str url: The URL to parse
        :rtype: :class:`ImageApiUrl`
        """
        url = urlunparse(
            urlparse(url)[0:3] + ("",)*3
        )
        return cls(
            parse_image_api_url_scheme_url_component(url),
            parse_image_api_url_server_url_component(url),
            parse_image_api_url_prefix_url_component(url),
            parse_image_api_url_identifier_url_component(url),
            parse_image_api_url_region_url_component(url),
            parse_image_api_url_size_url_component(url),
            parse_image_api_url_rotation_url_component(url),
            parse_image_api_url_quality_url_component(url),
            parse_image_api_url_format_url_component(url),
            validate=False
        )

    @classmethod
    def from_info_url(cls, url):
        """
        Instantiate an instance from an info URL

        :param str url: The URL to parse
        :rtype: :class:`ImageApiUrl`
        """
        url = urlunparse(
            urlparse(url)[0:3] + ("",)*3
        )
        return cls(
            parse_image_api_url_scheme_url_component(url),
            parse_image_api_url_server_url_component(url),
            parse_image_api_url_prefix_url_component(url),
            parse_image_api_url_identifier_url_component(url),
            validate=False
        )

    @classmethod
    def from_url(cls, url):
        """
        wraps :func:`ImageApiUrl.from_image_url` and :func:`ImageApiUrl.from_info_url`
        and tries to apply the correct one to any URL supplied.

        :param str url: The URL to parse
        :rtype: :class:`ImageApiUrl`
        """
        url = urlunparse(
            urlparse(url)[0:3] + ("",)*3
        )
        if url.endswith("info.json"):
            return cls.from_info_url(url)
        else:
            return cls.from_image_url(url)

    def __init__(self, scheme, server, prefix, identifier,
                 region="full", size="full", rotation="0",
                 quality="default", format="jpg", validate=True):
        """
        Instantiate a new instance.

        See `The IIIF Image API Specification <http://iiif.io/api/image/2.1/#uri-syntax>`_
        for explanations of each URI segment.

        :param str scheme: The scheme
        :param str server: The server
        :param str prefix: The prefix
        :param str identifier: The identifier
        :param str region: The region
        :param str size: The size
        :param str rotation: The rotation
        :param str quality: The qualty
        :param str format: The format
        :param bool validate: Whether or not to validate the record on creation.
        """
        self._scheme = scheme
        self._server = server
        self._prefix = prefix
        self._identifier = identifier
        self._region = region
        self._size = size
        self._rotation = rotation
        self._quality = quality
        self._format = format
        if validate:
            self.validate()

    def to_image_url(self):
        """
        Return a representation of the image url represented
        by the :class:`ImageApiUrl`

        :rtype: str
        """
        return self.scheme+"://" + self.server + self.prefix + "/" + \
            "/".join(
                [
                    self.identifier,
                    self.region,
                    self.size,
                    self.rotation,
                    self.quality
                ]
            ) + \
            ".{}".format(self.format)

    def to_info_url(self):
        """
        Return a representation of the info url represented
        by the :class:`ImageApiUrl`

        :rtype: str
        """
        return self.scheme+"://" + self.server + self.prefix + "/" + \
            self.identifier + "/info.json"

    def to_base_url(self):
        """
        Return a representation of the base url represented
        by the :class:`ImageApiUrl`

        :rtype: str
        """
        return self.scheme+"://" + self.server + self.prefix + "/" + \
            self.identifier

    def validate(self):
        """
        Validates the URL.

        Valid URLs will return None, invalid URLs will raise an exception

        :rtype: None
        """
        self.from_url(self.to_image_url())

    def set_scheme(self, x):
        old = self.scheme
        try:
            self._scheme = x
            self.validate()
        except ParameterError:
            self._scheme = old
            raise

    def get_scheme(self):
        return self._scheme

    def set_server(self, x):
        old = self.server
        try:
            self._server = x
            self.validate()
        except ParameterError:
            self._server = old
            raise

    def get_server(self):
        return self._server

    def set_prefix(self, x):
        if not x:
            self._prefix = ""
            return
        if not x.startswith("/"):
            raise ParameterError("Prefixes must start with '/'")
        old = self.prefix
        try:
            self._prefix = x
            self.validate()
        except ParameterError:
            self._prefix = old
            raise

    def get_prefix(self):
        return self._prefix

    def set_identifier(self, x, quote=True):
        if quote:
            x = quote(x, safe='')
        old = self.identifier
        try:
            self._identifier = x
            self.validate()
        except ParameterError:
            self._identifier = old
            raise

    def get_identifier(self):
        return self._identifier

    def set_region(self, x):
        old = self.region
        try:
            self._region = x
            self.validate()
        except ParameterError:
            self._region = old
            raise

    def get_region(self):
        return self._region

    def set_size(self, x):
        old = self.size
        try:
            self._size = x
            self.validate()
        except ParameterError:
            self._size = old
            raise

    def get_size(self):
        return self._size

    def set_rotation(self, x):
        old = self.rotation
        try:
            self._rotation = x
            self.validate()
        except ParameterError:
            self._rotation = old
            raise

    def get_rotation(self):
        return self._rotation

    def set_quality(self, x):
        old = self.quality
        try:
            self._quality = x
            self.validate()
        except ParameterError:
            self._quality = old
            raise

    def get_quality(self):
        return self._quality

    def set_format(self, x):
        old = self.format
        try:
            self._format = x
            self.validate()
        except ParameterError:
            self._format = old
            raise

    def get_format(self):
        return self._format

    scheme = property(get_scheme, set_scheme)
    server = property(get_server, set_server)
    prefix = property(get_prefix, set_prefix)
    identifier = property(get_identifier, set_identifier)
    region = property(get_region, set_region)
    size = property(get_size, set_size)
    rotation = property(get_rotation, set_rotation)
    quality = property(get_quality, set_quality)
    format = property(get_format, set_format)
