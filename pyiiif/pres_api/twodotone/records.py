"""Classes for building twodotone IIIF Presentation records:
"""

from os.path import join
import json
import requests
from urllib.parse import urlparse, ParseResult

from pyiiif.utils import escape_identifier, convert_context_url_into_lookup
from pyiiif.constants import valid_contexts, valid_viewingDirections, valid_viewingHints, valid_types
from pyiiif.image_api.twodotone import ImageApiUrl


# TODO define Annotation, ImageContent and OtherContent class methods

class Record:
    """
    A generic record class for IIIF Presentation records. This should not be called
    in any client code. Instead classes thatinherit record like Collection, 
    Manifest and Sequence and Canvas should be called

    :rtype :class:`Record`
    """
    __name__ = "Record"

    def __init__(self, *args, **kwargs):
        """initializes an instance of the class Record
        
        Since this is a generic record class this method does not do anything
        """
        pass 

    def __repr__(self):
        """a method to return a representation string of the object identifying it for debugging purposes

        An instance name is defined as the class name and (if available) the identifying URL for that instance 

        :rtype str
        :returns a string representing the name of the instance class 
        """
        out = self.__name__
        if getattr(self, 'id', None):
            out += " for " + self.id
        return out

    def __str__(self):
        """returns the object and all its property values as a dictionary that has been converted to a string

        :rtype str
        :returns a dictionary converted to a string with all properties names of the instance converted to IIIF keys
        """
        return json.dumps(self.to_dict())

    def _iterate_some_list(self, attribute_name):
        """a method to return a list of objects in an instance's property

        TODO: convert this to return just a list of string identifiers. Is this valuable extra abstraction?

        It first checks if the property being requested exists on the instance and if it does not raises a useful explanation in ValueError exception.
        If the property does exist, creates an empty list and iterates through the property adding the items to the new list.

        :param str attribute_name: the name of the property that the programmer wants to retrieve

        :rtype list
        :returns a list of objects
        """
        if hasattr(self, attribute_name):
            out = []
            for n_thing in getattr(self, attribute_name):
                out.append(n_thing)
            return out
        else:
            raise ValueError("this instance does not have the attribute {}".format(attribute_name))

    def _set_a_list_property(self, x, property_name, list_item_class):
        """a method to attempt to set a list value on a particular instance property

        Attempts to set the value of x onto the property defined with property_name. But, first
        it validates whether the value of x is a list and it validates whether all items in x are
        instances of the required class(es) for the property property_name. 

        Raises ValueError exceptions if any validation checks fail.

        :param str x: the list to set to the property
        :param str property_name: the name of the property to define
        :param str list_item_class: in situations where the items in a list can be more than one 
         class instances a list and in the eventuality that contained items can only be one class 
         instance a single class name
        """
        assert isinstance(x, list)
        for tally, n_col in enumerate(x):
            if isinstance(list_item_class, list):
                if not any([isinstance(n_col, i) for i in list_item_class]):
                    raise ValueError("item {} in inputted list is not a valid type for that list.".format(str(tally)))
            else:
                if not isinstance(n_col, list_item_class):
                    raise ValueError("item {} in inputted list is not an instance of {}".format(str(tally), list_item_class))
        setattr(self, property_name, x)

    def _get_simple_property(self, property_name):
        """a method to set a simple property value on an instance
        """
        if hasattr(self, property_name):
            return getattr(self, property_name)

    def _set_simple_property(self, x, property_name):
        """sets a simple property instance

        simple is defined as a string of alphanumeric characters

        :param str x: the value to set
        :param str properyt_name: the name of the property to set the value on
        """
        if isinstance(x, str):
            setattr(self, property_name, x)

    def _set_numeric_property(self, x, property_name):
        """sets a numeric property value on an instance 

        Checks if the value of x is indeed an integer. If x is not an integer, raises a ValueError exception
        
        :param str x: the value to set
        :param str property_name: the name of the property to set the value on
        """
        if isinstance(x, int):
            setattr(self, property_name, x)
        else:
            raise ValueError("{} is being set on {} which has to have a numeric value but it is {}".format(x, property_name, type(x).__name__))
        
    def _delete_a_property(self, property_name):
        if hasattr(self, "property_name"):
            self._manifests = None
        else:
            raise ValueError("{} hasn't been set on this instance".format(property_name))

    def _check_if_url_valid(self, url):
        """a method to check if an input url is well-formed or not

        Validates a URL string for properly formatted url according to RFC 1738. 

        taken from https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778

        :param str url: a string representing a live web resource.

        :rtype bool
        :return a boolean that asseses whether or not the url is a valid URL
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except:
            return False

    def _check_if_url_is_alive(self, url):
        """a method to check if url is alive

        Validates if a url is to a resolvable web resource. HTTP 404 counts as resolvable web resource.

        taken from  https://stackoverflow.com/questions/16778435/python-check-if-website-exists

        :param str url: a string representing a live web resource

        :rtype bool
        :return a boolean that asseses whether or not the url given is resolvable
        """
        response = requests.get(url, "HEAD")
        if not self._check_if_url_valid(url):
            return False
        if (response.status_code == 404) or (response.status_code < 400):
            return True
        else:
            return False

    def set_metadata(self, a_list):
        for n_item in a_list:
            if not isinstance(n_item, MetadataField):
                raise ValueError("metadata property can ony contain instances of MetadataField")
        self._metadata = a_list

    def get_metadata(self):
        return self._metadata

    def del_metadata(self):
        if hasattr(self, "_metadata"):
            self._metadata = None

    def get_type(self):
        """returns the type property value for an instance
        """
        return self._type

    def set_type(self, x):
        """sets the type property value of an instance

        Checks if the value of x is in the list of valid IIIF types as defined in constants.valid_types.
        If it is not in that list will raise a ValueError exception.

        :param str x: the value to set
        """
        if x in valid_types:
            self._type = x
        else:
            raise ValueError("{} is not a valid type for a IIIF record".format(x))

    def del_type(self, x):
        """sets the value of type property to None
        """
        self._type = None

    def get_id(self):
        """returns the value of the id property of an instance
        """
        return self._id

    def set_id(self, x):
        """sets the value of the id property of an instance

        Checks if the value of x is valid and it is alive. 
        If it is neither one or the other will raise a ValueError exception

        :param str x: a string representing a valid URL. 404 counts as valid
        """
        if self._check_if_url_valid(x) and self._check_if_url_is_alive(x):
            self._id = x
        else:
            raise ValueError("{} is not a valid url".format(x))

    def del_id(self):
        """sets a previously defined id property value to None
        """
        if self._id:
            self._id = None

    def get_context(self):
        """gets the value of the context property of an instance
        """
        return self._context

    def set_context(self, x):
        """defines the value of the context property of an instance

        Context is a very specific IIIF protocol. The value is one of two IIIF urls.
        So, ths method checks if the value of x is a valid key in the dictionary constants.valid_contexts
        If it is not it raises a ValueError exception; if it is it sets the value of context to the value of the 
        selected key in constants.valid_contexts

        :param str x: a string that is either 'image' or 'presentation'
        """
        if not hasattr(self, '_context') and isinstance(x, str):
            context = valid_contexts.get(x)
            if context:
                self._context = context
            else:
                raise ValueError("{} is not a valid context option for IIIF. It must be one of {}".\
                                 format(x, ', '.join(valid_contexts.keys())))
        else:
            raise ValueError("there is already a context set on this instance")

    def del_context(self):
        """sets a previously defined value of the context property to None
        """
        if self._context:
            self._context = None

    def get_viewingHint(self):
        """gets the value of the viewingHint property
        """
        return self._viewingHint

    def set_viewingHint(self, x):
        """sets the viewingHint property of an instance

        Checks if the value of x is in the list at constants.valid_viewHints. If it is not
        it raises a ValueError exception.

        :param str x: a IIIF viewingHint option
        """
        if x in valid_viewingHints:
            self._viewingHint = x
        else:
            raise ValueError("{} is not a valid viewingHint".format(x))

    def del_viewingHint(self):
        """sets a defined value of viewingHint to None
        """
        if self._viewingHint:
            self._viewingHint = None

    def get_viewingDirection(self):
        """gets the value of viewingDirection property of an instance

        :rtype str
        :returns viewingDirection
        """
        return self._viewingDirection

    def set_viewingDirection(self, x):
        """sets the value of the viewingDirection property of an instance

        Checks if the value of x is in the list at constants.valid_viewingDirections.
        If not, it raises a ValueError exception.

        :param str x: a IIIF viewingDirection option
        """
        if x in valid_viewingDirections:
            self._viewingDirection = x
        else:
            raise ValueError("{} is not a valid viewingDirection".format(x))

    def del_viewingDirection(self):
        """sets a previously defined value of viewingDirection property to None
        """
        if self._viewingDirection:
            self._viewingDirection = None

    def get_label(self):
        """returns the vlaue of the label property of an instance

        :rtype str
        :returns a string purporting to be the intellectual title of an instance
        """
        return self._label

    def set_label(self, x):
        """sets the value of the label property of an instance

        :param str x: an intellectual title for an instance
        """
        self._label = x

    def del_label(self):
        """sets the value of a previously defned label property to None
        """
        if self._label:
            self._label = None

    def get_description(self):
        """returns the value of property description

        :rtype str
        """
        return self._description

    def set_description(self, x):
        """sets the value of the description property

        This is the value of the description of a IIIF record and should adequately describe what 
        the intellectual object is, why it is signficant to a scholar.

        :rtype str x: a very long string potentially
        """
        self._description = x

    def del_description(self):
        """sets a previously defined value of property description to None
        """
        if self._description:
            self._description = None

    def _convert_context_url_into_lookup(self, a_url):
        pot_context = a_url
        for key, value in valid_contexts.items():
            if value == pot_context:
                return key

    def validate(self):
        """validate this record

        :rtype: tuple
        :returns a two part tuple: the first part is the Boolean value expressing whether or not the record is valid IIIF
        and the second part is the errors discovered in the IIIF record.
        """
        errors = []

        if not getattr(self, "id", None):
            errors.append("A IIIF record must have a valid id attribute")
        else:
            pass
        if not getattr(self, "type", None):
            errors.append("A IIIF record must have a valid type attribute")
        else:
            pass
        if (getattr(self, "viewingDirection", None)) and (getattr(self, "viewingDirection", None) not in valid_viewingDirections):
            errors.append("If viewingDirection is present on a IIIF record it must be valid direction")
        if (getattr(self, "viewingHint", None)) and (getattr(self, "viewingHint", None) not in valid_viewingHints):
            errors.append("If viewingHint is present on a IIIF record it must be valid hint")
        if errors:
            return (False, errors)
        else:
            return (True, errors)

    def to_dict(self):
        out = {}
        out["@id"] = self.id
        out["@type"] = self.type
        if hasattr(self, "context"):
            out["@context"] = self.context
        properties = vars(self)
        for n_property in properties:
            if n_property in ["_id", "_type", "_context"]:
                pass
            else:
                value = getattr(self, n_property, None)
                if isinstance(value, list):
                    if n_property == 'metadata':
                        out[n_property] = [x.to_dict() for x in getattr(self, n_property, None)]
                    else:
                        out[n_property[1:]] = [x.to_dict() for x in getattr(self, n_property, None)]
                if isinstance(value, str) or isinstance(value, int):
                    out[n_property[1:]] = getattr(self, n_property, None)
        return out

    type = property(get_type, set_type, del_type)
    id = property(get_id, set_id, del_id)
    context = property(get_context, set_context, del_context)
    viewingHint = property(get_viewingHint, set_viewingHint, del_viewingHint)
    viewingDirection = property(get_viewingDirection, set_viewingDirection, del_viewingDirection)
    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)

class ServerProfile(object):
    """a class for building IIIF Collection ServerProfile information on an Service instance

    This class should not normally be called independentaly of the Service class.
    """
    __name__ = "IIIF ServerProfile"

    def __init__(self):
        """initializes an instance of the class

        Right now it is hard-coded to set supports, qualities and formats with generic IIIF 2.0 compliant values

        TODO: allow dynamic loading of this information 

        :rtype :class:`ServerProfile`
        """
        self.supports = ["canonicalLinkHeader",
                         "profileLinkHeader",
                         "mirroring",
                         "rotationAboveArbitrary",
                         "regionSquare",
                         "sizeAboveFull"
                        ]
        self.qualities = ["default", "gray", "bitonal"]
        self.format = ["jpg", "png", "gif", "webp"]

    def to_dict(self):
        """a method to transform the instance into a dictionary 
        """
        out = {}
        out["supports"] = self.supports
        out["qualities"] = self.qualities
        out["format"] = self.format       
        return out        


class Service(Record):
    """a class for building IIIF Server information on a ServerProfile instance

    This class should not normally be called independantly of the ImageResource class.
    """

    def __init__(self, uri):
        """initializes an instance of the class

        It takes the uri passed to it from the instantiating ImageResource
        and sets the id of the instance

        :param str uri: a string representing a resolvable IIIF Image API resource

        :rtype :class:`ServerProfile`
        """

        self.id = uri
        self.context = "image"
        self.profile = ServerProfile()

    def to_dict(self):
        """a method to transform the instance into a dictionary 
        """
        out = {}
        out["@id"] = self.id
        out["@context"] = self.context
        out["profile"] = ["https://iiif.io/api/image/2/level2.json",
                          self.profile.to_dict()]
        return out

class ImageResource(Record):
    """a class to represent a IIIF Presentation ImageResource 

    Use this in your annotations that require it and swap them in and out of
    annotations as you see fit.
    """
    __name__ = "ImageResource"

    def __init__(self, scheme, server_host, prefix, identifier, mimetype):
        """instantiate a new instance

        :param str scheme: the protocol over which the web request should go: 
         usually either http or https
        :param str server_host: the host on which your iiif image server runs. 
         Frequently called the domain name
        :param str prefix: an extra path variable, typicaly an alias on your url 
         that your host needs to be able to forward the request to your image api service
        :param str identifier: the id of the image that you are requesting. 
         Ex. 'apf/2/apf2-00001.tif' or 'super-secret-identified-image'
        :param str mimetype: the mimetype of the image you are serving 

        :rtype :class:`ImageResource`
        """
        url = ImageApiUrl(scheme, server_host, prefix, identifier)
        #url = ParseResult(scheme="https", netloc=server_host,
        #                  path=join("/", escape_identifier(identifier)), params="", query="", fragment="")
        try:
            r = requests.get(url.to_info_url(), "HEAD")
            data = r.json()
            data["@context"]
            data["@id"]
        except:
            raise ValueError("{} is not a IIIF Image API url".format(url.to_info_url()))
        self.id = url.to_image_url() 
        self.type = "dctypes:Image"
        self.format = mimetype
        self.service = Service(url.to_base_url())

    def get_format(self):
        """gets the format property of the instance

        The format is the mimetype of the source of the image being requested from a IIIF Image API

        :rtype str
        :returns a string representing the mimetype of the source of the image being defined
        """
        return self._get_simple_property("_format")

    def set_format(self, x):
        """sets the format property of the instance

        See http://www.ietf.org/rfc/rfc2045.txt and http://www.ietf.org/rfc/rfc2046.txt 
        for more information about mimetypes
       
        TODO: write proper mimetype validation if this is not too hairy of a problem to solve!

        :param str x: the mimetype of source image conforming to RFC 2045 and RFC 2046
        """
        self._set_simple_property(x, "_format")

    def del_format(self):
        """sets the format property to null
        """
        self._delete_a_property("_format")

    def get_height(self):
        """gets the height property of the instance

        The height is the mimetype of the source of the image being requested from a IIIF Image API

        :rtype str
        :returns a string representing the mimetype of the source of the image being defined
        """
        return self._get_numeric_property("_height")

    def set_height(self, x):
        """sets the height property of the instance

        See http://www.ietf.org/rfc/rfc2045.txt and http://www.ietf.org/rfc/rfc2046.txt 
        for more inheightion about mimetypes
       
        TODO: write proper mimetype validation if this is not too hairy of a problem to solve!

        :param str x: the mimetype of source image conforming to RFC 2045 and RFC 2046
        """
        self._set_numeric_property(x, "_height")

    def del_height(self):
        """sets the height property to null
        """
        self._delete_a_property("_height")

    def get_service(self):
        """returns the service property of the instance

        """
        if getattr(self, "_service", None):
            return self._service

    def set_service(self, x):
        """sets the service property of the instance
        """
        self._service = x

    def del_service(self):
        """sets a previously defined service property of an instance to None
        """
        self._delete_a_property("_service")

    def get_width(self):
        """gets the width property of the instance

        The width is the mimetype of the source of the image being requested from a IIIF Image API

        :rtype str
        :returns a string representing the mimetype of the source of the image being defined
        """
        return self._get_numeric_property("_width")

    def set_width(self, x):
        """sets the width property of the instance

        See http://www.ietf.org/rfc/rfc2045.txt and http://www.ietf.org/rfc/rfc2046.txt 
        for more inwidthion about mimetypes
       
        TODO: write proper mimetype validation if this is not too hairy of a problem to solve!

        :param str x: the mimetype of source image conforming to RFC 2045 and RFC 2046
        """
        self._set_numeric_property(x, "_width")

    def del_width(self):
        """sets the width property to null
        """
        self._delete_a_property("_width")

    def to_dict(self):
        """converts an instance to a dictionary

        :rtype dict
        :returns A dictionary data structure with key names conforming to IIIF specification 
         containing all defined properties
        """
        out = {}
        out["@id"] = self.id
        out["@type"] = self.type
        out["format"] = self.format
        out["height"] = self._height
        out["service"] =  self.service.to_dict()
        out["width"] =  self._width
        return out

    @classmethod
    def load(cls, json_data):
        """a method to  instantiate an instance from a JSON string

        :param string json_data: a string of valid JSON data containing information about a IIIF Resource

        :rtype :class:`ImageResource`
        """
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("invalid JSON was passed to ImageResource.load()")
        identifier = data.get("@id")
        image_url = ImageApiUrl.from_image_url(identifier)
        i = cls(image_url.scheme, image_url.server, image_url.prefix, image_url.identifier, data.get("format"))
        i.format = data.get("format")
        i.type = data.get("@type")
        i.service = data.get("service")
        return i

    service = property(get_service, set_service, del_service)
    format = property(get_format, set_format, del_format)

class Collection(Record):
    """a class for building IIIF Collection records
    """

    __name__ = "Collection"

    def __init__(self, uri):
        """"initializes a Collection with type sc:Collection and id of uri given at init

        :param str url: the  url for the collection IIIF record

        :rtype :class:`Collection`
        """
        self.context = "presentation"
        self.type = "sc:Collection"
        self.id = uri

    def __repr__(self):
        """a method to return a representation of the instance

        :rtype str
        :returns a string defining the object as a Collection with the id of that collection
        """
        return "<Collection record for {} >".format(self.id)

    def get_collections(self):
        """gets the collections that have been added to the instance

        :rtype list
        :returns a list of objects that are contained in the collections property
        """
        return self._iterate_some_list('_collections')

    def set_collections(self, x):
        """sets the collections property for the instance

        WARNING: any members of this list can only be Manifest instances
        """
        self._set_a_list_property(x, '_collections', Collection)

    def del_collections(self):
        """sets the collection property to None if it has been set already
        """
        if hasattr(self, "_collections"):
            self._collections = None

    def get_manifests(self):
        """gets the manifests that have been added to the instance

        :rtype list
        :returns a list of objects that are contained in the manifests property
        """
        return self._iterate_some_list('_manifests')

    def set_manifests(self, x):
        """sets the manifests property of the instance

        WARNING: any members of this list can only be Manifest instances
        """
        self._set_a_list_property(x, '_manifests', Manifest)

    def del_manifests(self):
        """sets the manifests property to None if it has been set already
        """   
        self._delete_a_property("_manifests")

    def get_members(self):
        return self._iterate_some_list('_members')

    def set_members(self, x):
        """sets the manifests property of the instance

        WARNING: any members of this list can only be either Manifest or Collection instances
        """
        self._set_a_list_property(x, '_members', [Manifest, Collection])

    def del_members(self):
        """sets the members property to None if it has been set already
        """
        if hasattr(self, "_members"):
            self._manifests = None
        else:
            raise ValueError("members hasn't been set on this instance")

    @classmethod
    def load(cls, json_data):
        """a class method to instantiate an instance of Collection class from a json string

        :rtype :class:`Collection`
        """
        try:
            data = json.dumps(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("Sequence.load() was passed invalid JSON data")
        new_collection = cls(data.get("@id"))
        if data.get("description"):
            new_collection.description = data.get("description")
        if data.get("label"):
            new_collection.label = data.get("label")
        if data.get("viewingDirection"):
            new_collection.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_collection.viewingHint = data.get("viewingHint")

        if data.get("metadata"):
            mdata_list = []
            for a_field in data.get("metadata"):
                new_field = MetadataField(a_field.get("label"), a_field.get("value"))
                mdata_list.append(new_field)
            new_collection.metadata = mdata_list 
        if data.get("members"):
            members_list = []
            for member in data.get("members"):
                the_type = member.get("@type")
                if the_type == "sc:Manifest":
                    new_member = Manifest.load(member)
                elif the_type == "sc:Collection":
                    new_member = Collection.load(member)
                else:
                    raise ValueError("Manifest was passed invalid IIIF members list")
                new_member.type = the_type
                members_list.append(new_member)
            new_collection.members = members_list
        if data.get("collections"):
            collections = []
            for collection in data.get("collections"):
                the_type = member.get("@type")
                if the_type == "sc:Collection":
                    new_member = Collection.load(collection)
                else:
                    raise ValueError("Manifest was passed invalid IIIF members list")
                new_member.type = the_type
                collections.append(new_member)
            new_collection.collections = collections
        if data.get("manifests"):
            manifests = []
            for manifest in data.get("manifests"):
                the_type = member.get("@type")
                if the_type == "sc:Manifest":
                    new_member = Manifest.load(manifest)
                else:
                    raise ValueError("Manifest was passed invalid IIIF members list")
                new_member.type = the_type
                manifest.append(new_member)
            new_collection.manifests = manifests
        return new_collection

    collections = property(get_collections, set_collections, del_collections)
    manifests = property(get_manifests, set_manifests, del_manifests)
    members = property(get_members, set_members, del_members)


class Manifest(Record):
    """a class for building IIIF Manifest records
    """
    __name__ = "Manifest"    

    def __init__(self, uri):
        """"initializes a Manifest with type sc:Manifest and id of uri given at init

        :param str url: the  url for the manifest IIIF record

        :rtype :class:`Manifest`
        """

        self.context = "presentation"
        self.type = "sc:Manifest"
        self.id = uri

    def get_sequences(self):
        """a method to get the value of the sequences property

        It will return a list of the objects of type Sequence

        :rtype list
        """
        return self._iterate_some_list("_sequences")

    def set_sequences(self, x):
        """a method to set the value of the sequences property. 
        
        Every instance in the list must be of type Sequence. If any item is not of type Sequence 
        will raise a ValueError exception
        """
        self._set_a_list_property(x, "_sequences", Sequence)
        pass

    def del_sequences(self):
        """a method to set the value of sequences to None
        """
        self._delete_a_property("_sequences")

    def get_structures(self):
        """a method to get the value of structures property

        It will return a list of objects of type Structure

        :rytpe list
        """
        return self._iterate_some_list("_structures")

    def set_structures(self, x):
        """a method to set the value of the structures property. 
        
        Every instance in the list is of type Range. If any item is not of type Range 
        will raise a ValueError exception
        """
        self._set_a_list_property(x, "_structures", Range)

    def del_structures(self):
        """a method to set the value of structures property to None
        """
        self._delete_a_property("_structures")

    @classmethod
    def load(cls, json_data):
        """a class method to instantiate an instance of Manifest class from a json string

        :rtype :class:`Manifest`
        """
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("Sequence.load() was passed invalid JSON data")
        new_manifest = cls(data.get("@id"))
        if data.get("metadata"):
            mdata_list = []
            for a_field in data.get("metadata"):
                new_field = MetadataField(a_field.get("label"), a_field.get("value"))
                mdata_list.append(new_field)
            new_manifest.metadata = mdata_list 
 
        if data.get("description"):
            new_manifest.description = data.get("description")
        if data.get("label"):
            new_manifest.label = data.get("label")
        if data.get("viewingDirection"):
            new_manifest.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_manifest.viewingHint = data.get("viewingHint")
        if data.get("sequences"):
            sequence_list = []
            for sequence in data.get("sequences"):
                new_sequence = Sequence.load(json.dumps(sequence))
                sequence_list.append(new_sequence)
            new_manifest.sequences = sequence_list
        if data.get("structures"):
            structures_list = []
            for structure in data.get("structures"):
                new_structure = Range.load(json.dumps(structure))
                structures_list.append(new_structure)
            new_manifest.structures = structures_list
        return new_manifest

    sequences = property(get_sequences, set_sequences, del_sequences)
    structures = property(get_structures, set_structures, del_structures)


class Sequence(Record):
    """a class for building IIIF Sequence records
    """
    __name__ = "Sequence"

    def __init__(self, uri):
        """initializes an instance of class Sequence

        :param str uri: a string representing a resolvable url 

        :rtype :class:`Sequence`
        """
        self.id = uri
        self.type = "sc:Sequence"
        self.canvases = []

    def get_canvases(self):
        """a method to return the value of the canvases property

        Returns a list of Canvas objects

        :rtype list
        """
        return self._iterate_some_list("_canvases")

    def set_canvases(self, x):
        """a method to set the value of the canvases property

        :param list x: a list of objects all of type Canvas
        """
        self._set_a_list_property(x, "_canvases", Canvas)

    def del_canvases(self):
        """a method to set the value of canvases property to None
        """
        self._delete_a_property("_canvases")

    def del_canvas(self, a_canvas):
        """a method to delete a canvas from a sequence

        takes a canvas object, checks if that object exists in the sequence
        and if it does deletes it from the list.
        """
        if getattr(self, "_canvas", None):
            the_list = getattr(self, "_canvases")
            pos_to_remove = the_list.index(a_canvas)
            del the_list[pos_to_remove]
            self._set_a_list_property(the_list, "_canvases", Canvas)

    @classmethod
    def load(cls, json_data):
        """a class method to instantiate an instance of Sequence class from a json string

        :rtype :class:`Sequence`
        """
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("Sequence.load() was passed invalid JSON data")
        new_sequence = Sequence(data.get("@id"))
        if data.get("description"):
            new_sequence.description = data.get("description")
        if data.get("label"):
            new_sequence.label = data.get("label")
        if data.get("startCanvas"):
            new_sequence.startCanvas = data.get("startCanvas")
        if data.get("viewingDirection"):
            new_sequence.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_sequence.viewingHint = data.get("viewingHint")
        if data.get("canvases"):
            canvas_list = []
            for canvas in data.get("canvases"):
                new_canvas = Canvas.load(json.dumps(canvas))
                canvas_list.append(new_canvas)
            new_sequence.canvases = canvas_list
        return new_sequence

    canvases = property(get_canvases, set_canvases, del_canvases)


class Canvas(Record):
    """a class for building IIIF Canvas records
    """
    __name__ = "Canvas"

    def __init__(self, uri):
        """initializes an instance of class Canvas

        :param str uri: a string representing a resolvable url 

        :rtype :class:`Canvas`
        """
        self.id = uri
        self.type = "sc:Canvas"

    def get_images(self):
        """a method to return the value of the images property

        Returns a list of ImageResource objects

        :rtype list
        """
        return self._iterate_some_list("_images")

    def set_images(self, x):
        """a method to set the value of the canvases property

        :param list x: a list of objects all of type Canvas
        """
        self._set_a_list_property(x, "_images", Annotation)

    def del_images(self):
        """a method to set the value of canvases property to None
        """
        self._delete_a_property("_images")

    def get_otherContent(self):
        """a method to return the value of the otherContent property

        Returns a list of AnnotationList objects

        :rtype list
        """
        return self._iterate_some_list("_otherContent")

    def set_otherContent(self, x):
        """a method to set the value of the otherContent property

        :param list x: a list of objects all of type AnnotationList
        """
        self._set_a_list_property(x, "_otherContent", AnnotationList)

    def del_otherContent(self):
        """a method to set the value of otherContent property to None
        """
        self._delete_a_property("_otherContent")

    def get_height(self):
        """a method to get the value of the height property

        :rtype int
        """
        return self._get_simple_property("_height")

    def set_height(self, x):
        """a method to set the value of the height property

        :param int x
        """
        self._set_numeric_property(x, "_height")

    def del_height(self):
        """a method to set the value of the height property to None
        """
        self._delete_a_property("_height")

    def get_width(self):
        """a method to get the value of the width property

        :rtype int
        """
        return self._get_simple_property("_width")

    def set_width(self, x):
        """a method to set the value of of the width property

        :param int x
        """
        self._set_numeric_property(x, "_width")

    def del_width(self):
        """a method to set the value of the width property to None
        """
        self._delete_a_property("_width")

    def validate(self):
        """a method to validate the Canvas object as IIIF compliant
        """
        if hasattr(self, 'height') and hasattr(self, 'width') and hasattr(self, 'label') and hasattr(self, 'images'):
            return True
        else:
            return False

    @classmethod
    def load(cls, json_data):
        """a class method to instantiate an instance of Canvas class from a json string

        :rtype :class:`Canvas`
        """
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("Canvas.load was passed invalid json data")
        img_list = []
        new_canvas = cls(data.get("@id"))
        if data.get("description"):
            new_canvas.description = data.get("description")
        new_canvas.label = data.get("label")
        new_canvas.height = data.get("height")
        new_canvas.width = data.get("width")
        if data.get("images"):
            for n in data.get("images"):
                an_annotation = Annotation.load(json.dumps(n), on=data.get("@id"))
                img_list.append(an_annotation)
            new_canvas.images = img_list
        if data.get("otherContent"):
            otherContent = [] 
            for oContent in data.get("otherContent"):
                new_oContent = OtherContent.load(json.dumps(oContent))
                otherContent.append(new_oContent)
            new_canvas.otherContent = otherContent
        return new_canvas

    images = property(get_images, set_images, del_images)
    height = property(get_height, set_height, del_height)
    width = property(get_width, set_width, del_width)
    otherContent = property(get_otherContent, set_otherContent, del_otherContent)

class AnnotationList(Record):
    """a class for building IIIF AnnotationList records

    """
    __name__ = "AnnotationList"

    def __init__(self, uri):
        """initializes an instance of AnnotationList

        :param str url: a valid url meant to identify the AnnotationList

        :rtype :class:`AnnotationList`
        """
        self.id = uri
        self.type = "sc:AnnotationList"

    def get_resources(self):
        """returns the value of the resources property

        :rtype list
        :returns a list of Annotation instances
        """
        return self._iterate_some_list("_resources")

    def set_resources(self, x):
        """sets the value of the resource property

        :param list x: a list of Annotation instances
        """
        return self._set_a_list_property(x, "_resources", Annotation)

    def del_resources(self):
        """sets teh value of resources property to None if the property has been previously set
        """
        self._delete_a_property("_resources")

    def get_on(self):
        return self._get_simple_property("_on")

    def set_on(self, x):
       self._set_simple_property(x, '_on')

    def del_on(self):
        self._delete_a_property("_on")


    def to_dict(self):
        """converts an instance to a dictionary

        :rtype dict
        :returns A dictionary data structure with key names conforming to IIIF specification 
         containing all defined properties
        """
        out = {}
        out["@id"] = self.id
        out["@type"] = self.type
        out["resources"] = []
        if hasattr(self, "resources", None):
            for resource in self.resources:
                n_item = resource.to_dict()
                out["resources"].append(n_item)
        return out

    def __str__(self):
        return str(self.to_dict())

    @classmethod
    def load(cls, json_data):
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("bad JSON passed to AnnotationList.load()")
        new_annotation_list = cls(data.get("@id"))
        if data.get("description"):
            new_annotation_list.description = data.get("description")
        if data.get("label"):
            new_annotation_list.label = data.get("label")
        if data.get("viewingDirection"):
            new_annotation_list.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_annotation_list.viewingHint = data.get("viewingHint")
        if data.get("resources"):
            new_resource_list = []
            for resource in data.get("resources"):
                new_anno = Annotation.load(json.dumps(resource))
                new_resource_list.append(new_anno)
            new_annotation_list.resources = new_resource_list
        return new_annotation_list

    resources = property(get_resources, set_resources, del_resources)
    on = property(get_on, set_on, del_on)

class Annotation(Record):
    """a class for building IIIF Annotation records

    """
    __name__ = "Annotation"

    def __init__(self, uri, on):
        """initializes an instance of Annotation

        :param str url: a valid url meant to identify the Annotation

        :rtype :class:`Annotation`
        """
        self.id = uri
        self.type = "oa:Annotation"
        self.motivation = "sc:Painting"
        self.on = on

    def get_format(self):
        """returns the value of the resources property

        :rtype list
        :returns a list of Annotation instances
        """

        return self._get_simple_property("_format")

    def set_format(self, value):
        self._set_simple_property(value, "_format")

    def del_format(self):
        self._delete_a_property("_format") 

    def get_resource(self):
        """returns the value of the resource property

        :rtype :class:`ImageResource`
        :returns an instance of ImageResource
        """
        return self._get_simple_property("_resource")

    def set_resource(self, x):
        """sets the value of the resource property

        If the parameter 'x' is not an instance of ImageResource will raise a ValueError exception

        :param ImageResource x: an intance of the ImageResource class
        """
        if isinstance(x, ImageResource):
            self._resource = x

    def del_resource(self):
        """sets a previously set value of the resource property to None
        """
        self._delete_a_property("_resource")

    def get_motivation(self):
        """returns the value of the motivation property

        :rtype str
        """
        return self._get_simple_property("_motivation")

    def set_motivation(self, x):
        """sets the value of the motivation property

        :param str x: a valid IIIF motivation for an Annotation
        """
        self._set_simple_property(x, "_motivation")

    def del_motivation(self):
        """sets the previously defined value of the motivation property to None
        """
        self._delete_a_property("_motivation")

    def to_dict(self):
        """converts an instance to a dictionary

        :rtype dict
        :returns A dictionary data structure with key names conforming to IIIF specification 
         containing all defined properties
        """
        out = {}
        out["@id"] = self.id
        out["@type"] = self.type
        out["motivation"] = self.motivation
        if getattr(self, "resource", None):
            out["resource"] = self.resource.to_dict()
        out["on"] = self.on
        return out

    @classmethod
    def load(cls, json_data, on=None):
        try:
            data = json.loads(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("bad JSON passed to Annotation.load()")
        new_annotation = cls(data.get("@id"))
        if on:
            new_annotation.on = on
        if data.get("description"):
            new_annotation.description = data.get("description")
        if data.get("label"):
            new_annotation.label = data.get("label")
        if data.get("viewingDirection"):
            new_annotation.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_annotation.viewingHint = data.get("viewingHint")
        if data.get("format"):
            new_annotation.format = data.get("format")
        if data.get("motivation"):
            new_annotation.motivation = data.get("motivation")
        if data.get("resource"):
            img_url = data.get("resource").get("@id")
            img_api_url = ImageApiUrl.from_image_url(img_url)
            new_img_resource = ImageResource(img_api_url.scheme, img_api_url.server,
                                             img_api_url.prefix, img_api_url.identifier,
                                             data.get("resource").get("format"))
            new_annotation.resource = new_img_resource
        return new_annotation

    format = property(get_format, set_format, del_format)
    resource = property(get_resource, set_resource, del_resource)
    motivation = property(get_motivation, set_motivation, del_motivation)

class Range(Record):
    """a class for building IIIF Annotation records

    """
    __name__ = "Range"

    def __init__(self, uri):
        """initializes an instance of Range

        :param str url: a valid url meant to identify the AnnotationList

        :rtype :class:`Range`
        """
        self.id = uri
        self.type = "sc:Range"
        
    def get_canvases(self):
        """returns the value of the canvases property

        Returns a list of Canvas instances

        :rtype list
        """
        return self._iterate_some_list("_canvases")

    def set_canvases(self, x):
        """sets the value of the canvases property

        If x contains any instance that is not of the Canvas class will raise a ValueError exception

        :param x list: a list of Canvas instances
        """
        return self._set_a_list_property(x, "_canvases", Canvas)

    def del_canvases(self):
        """sets previously defined canvases property to None
        """
        self._delete_a_property("_canvases")

    def get_members(self):
        """returns the value of the members property

        Returns a list of either Canvas or Range instances

        :rtype list
        """
        return self._iterate_some_list("_members")

    def set_members(self, x):
        """sets the value of the canvases property

        If x contains any instance that is not of the Canvas class will raise a ValueError exception

        :param x list: a list of Canvas instances
        """
 
        return self._set_a_list_property(x, "_members", [Canvas, Range])

    def del_members(self):
        """sets previously defined members property to None
        """
 
        self._delete_a_property("_members")

    def get_ranges(self):
        """returns the value of the ranges property

        Returns a list of Range instances

        :rtype list
        """
        return self._iterate_some_list("_ranges")

    def set_ranges(self, x):
        """sets the value of the ranges property

        If x contains any instance that is not of the Range class will raise a ValueError exception

        :param x list: a list of Range instances
        """
 
        return self._set_a_list_property(x, "_ranges", Range)

    def del_ranges(self):
        """sets previously defined members property to None
        """
        self._delete_a_property("_ranges")

    @classmethod
    def load(cls, json_data):
        try:
            data = json.dumps(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("bad JSON passed to Range.load()")
        new_range = cls(data.get("@id"))
        if data.get("description"):
            new_range.description = data.get("description")
        if data.get("label"):
            new_range.label = data.get("label")
        if data.get("viewingDirection"):
            new_range.viewingDirection = data.get("viewingDirection")
        if data.get("viewingHint"):
            new_range.viewingHint = data.get("viewingHint")
        if data.get("canvases"):
            new_canvases = []
            for canvas in data.get("canvases"):
                new_canvas = Canvas.load(json.dumps(canvas))
                new_canvases.append(new_canvas)
            new_range.canvases = new_canvases
        if data.get("members"):
            new_members = []
            for member in data.get("members"):
                if member.get("@type") == "sc:Range":
                    new_member = Range.load(json.dumps(canvas))
                elif member.get("@type") == "sc:Canvas":
                    new_member = Canvas.load(json.dumps(canvas))
                else:
                    raise ValueError("A member in imported JSON members property has invalid @type")
                new_members.append(new_member)
            new_range.member = new_members
        if data.get("ranges"):
            new_ranges = []
            for a_range in data.get("ranges"):
                new_range = Canvas.load(json.dumps(a_range))
                new_ranges.append(new_range)
            new_range.member = new_ranges
 
    canvases = property(get_canvases, set_canvases, del_canvases)
    members = property(get_members, set_members, del_members)
    ranges = property(get_ranges, set_ranges, del_ranges)

class OtherContent(object):
    """a class for building IIIF otherContent
    """
    __name__ = "OtherContent"

    def __init__(self, x):
        """initializes an instance of OtherContent

        :param str x: a list of valid urls

        :rtype :class:`OtherContent`
        """
        self.items = x

    def set_items(self, x):
        """sets the value of the items property 

        Each list item must be a resolvable URL

        :param str x: a list of urls

        """
        for n_url in x:
            u = requests.get(x, "HEAD")
            if u.status_code() == 200:
                pass
            else:
                raise ValueError("{} is not a valid url for otherContent".format(n_url))
        self._items = x    

    def get_items(self):
        """returns the value of the items property

        :rtype list
        """
        out = []
        for n_item in self.items:
            out.append(n_item)
        return out

    def del_items(self):
        """sets the previously set items property to None
        """
        self._items = None

    def to_dict(self):
        return {"otherContent": self.items}

    @classmethod
    def load(cls, json_data):
        try:
            data = json.load(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("OtherContent.load got invalid JSON data")
        return cls(data)

    items = property(get_items, set_items, del_items)

class MetadataField:
    """a class for building IIIF MetadataField
    """
    __name__ = "MetadataField"

    def __init__(self, label, value):
        """initializes an instance of MetadataField

        :param str label: a human-readable string describing what a particular metadata field represents
        :param str value: a value for a particular metadata field

        :rtype :class:`MetadataField`
        """
        self.label = label
        self.value = value

    def get_label(self):
        return getattr(self, "_label", None)

    def set_label(self, x):
        setattr(self, "_label", x)     

    def del_label(self):
        setattr(self, "_label", None) 

    def get_value(self):
        return getattr(self, "_value", None)

    def set_value(self, x):
        setattr(self, "_value", x)     

    def del_value(self):
        setattr(self, "_label", None) 

    def to_dict(self):
        return {"label": self.label, "value": self.value}

    @classmethod
    def load(cls, json_data):
        try:
            data = json.load(json_data)
        except json.decoder.JSONDecodeError:
            raise ValueError("MetadataField.load got invalid JSON data")
        return cls(data.get("label"), data.get("value"))



    label = property(get_label, set_label, del_label)
    value = property(get_value, set_value, del_value)

# JSON-LD @types to Class; used for converting the string value in 
# @type loading JSON strings into the right object instances
ttc = {
    "sc:Collection": Collection,
    "sc:Manifest": Manifest,
    "sc:Sequence": Sequence,
    "sc:Canvas": Canvas,
    "oa:Annotation": Annotation,
    "sc:AnnotationList": AnnotationList,
    "sc:Range": Range,
    "dctypes:Image": ImageResource
}
