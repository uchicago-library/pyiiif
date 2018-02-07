"""
pyiiif: Library code for working with the IIIF specifications
"""

__author__ = "Brian Balsamo"
__email__ = "brian@brianbalsamo.com"
__version__ = "0.0.1"

import re
import urllib.parse

from .constants import valid_image_formats, valid_schemes
from .exceptions import ParameterError



# {scheme}://{server}{/prefix}/{identifier}/{region}/{size}/{rotation}/{quality}.{format}


class ImageApiUrl:
    """
    A class for parsing, creating, and manipulating IIIF Image API URLs
    """
    @classmethod
    def parse_scheme_url_component(cls, url):
        scheme = urllib.parse.urlparse(url).scheme
        if scheme not in valid_schemes:
            raise ParameterError(
                "Valid schemes include: {}".format(", ".join(valid_schemes))
            )
        return scheme

    @classmethod
    def parse_server_url_component(cls, url):
        return urllib.parse.urlparse(url).netloc

    @classmethod
    def parse_prefix_url_component(cls, url):
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

    @classmethod
    def parse_identifier_url_component(cls, url):
        if url.endswith("info.json"):
            p = urllib.parse.urlparse(url).path
            s = p.split("/")[-2]
            return s
        else:
            p = urllib.parse.urlparse(url).path
            s = p.split("/")[-5]
            return s

    @classmethod
    def parse_region_url_component(cls, url):
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
                    raise ParameterError("Incorrect region paramter")
            return s
        # region=pct:41.6,7.5,40,70
        elif s.startswith("pct:"):
            for x in s[4:].split(","):
                try:
                    float(x)
                except ValueError:
                    raise ParameterError("Incorrect region paramter")
            return s
        # Error case
        else:
            raise ParameterError("Incorrect region parameter")

    @classmethod
    def parse_size_url_component(cls, url):
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

    @classmethod
    def parse_rotation_url_component(cls, url):
        # .../full/full/0/default.jpg
        # .../full/full/!0/default.jpg
        p = urllib.parse.urlparse(url).path
        s = p.split("/")[-2]
        if s.startswith("!"):
            if len(s) < 2:
                raise ParameterError("Incorrect rotation paramter")
            c = s[1:]
        else:
            c = s
        try:
            assert(0 <= float(c) <= 360)
            return s
        # Error case
        except (ValueError, AssertionError):
            raise ParameterError("Incorrect rotation parameter")

    @classmethod
    def parse_quality_url_component(cls, url):
        p = urllib.parse.urlparse(url).path
        subp = p.split("/")[-1]
        qual = subp.split(".")[0]
        if qual in ("color", "gray", "bitonal", "default"):
            return qual
        else:
            raise ParameterError("Incorrect quality parameter")

    @classmethod
    def parse_format_url_component(cls, url):
        p = urllib.parse.urlparse(url).path
        fmt = p.split(".")[-1]
        if fmt in valid_image_formats:
            return fmt
        else:
            raise ParameterError("Incorrect format paramter")

    @classmethod
    def from_image_url(cls, url):
        url = urllib.parse.urlunparse(
            urllib.parse.urlparse(url)[0:3] + ("",)*3
        )
        return cls(
            cls.parse_scheme_url_component(url),
            cls.parse_server_url_component(url),
            cls.parse_prefix_url_component(url),
            cls.parse_identifier_url_component(url),
            cls.parse_region_url_component(url),
            cls.parse_size_url_component(url),
            cls.parse_rotation_url_component(url),
            cls.parse_quality_url_component(url),
            cls.parse_format_url_component(url),
            validate=False
        )

    @classmethod
    def from_info_url(cls, url):
        url = urllib.parse.urlunparse(
            urllib.parse.urlparse(url)[0:3] + ("",)*3
        )
        return cls(
            cls.parse_scheme_url_component(url),
            cls.parse_server_url_component(url),
            cls.parse_prefix_url_component(url),
            cls.parse_identifier_url_component(url),
            validate=False
        )

    @classmethod
    def from_url(cls, url):
        url = urllib.parse.urlunparse(
            urllib.parse.urlparse(url)[0:3] + ("",)*3
        )
        if url.endswith("info.json"):
            return cls.from_info_url(url)
        else:
            return cls.from_image_url(url)

    def __init__(
        self, scheme, server, prefix, identifier,
        region="full", size="full", rotation="0",
        quality="default", format="jpg", validate=True
    ):
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
        return self.scheme+"://" + self.server + self.prefix + "/" + \
            self.identifier + "/info.json"

    def validate(self):
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
            x = urllib.parse.quote(x, safe='')
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
