"""Classes for building twodotone IIIF Presentation records
"""

import json
import requests
from urllib.parse import urlparse

from pyiiif.constants import valid_contexts, valid_viewingDirections, valid_viewingHints, valid_types

# TODO define Annotation, ImageContent and OtherContent class methods

class Record:
    """
    A generic record class for IIIF Presentation records. This should not be called
    in any client code. Instead classes thatinherit record like Collection, 
    Manifest and Sequence and Canvas should be called
    """
    def __init__(self, *args, **kwargs):
        pass 

    def __str__(self):
        out = {}
        out["@id"] = self.id
        out["@type"] = self.type
        if hasattr(self, 'context'):
            out["@context"] = self.context
        if hasattr(self, 'viewingHint'):
            out["viewingHint"] = self.viewingHint
        if hasattr(self, 'viewingDirection'):
            out["viewingDirection"] = self.viewingDirection
        if hasattr(self, 'label'):
            out["label"] = self.label
        if hasattr(self, 'description'):
            out["description"] = self.description
        return json.dumps(out)

    def _iterate_some_list(self, attribute_name):
        if hasattr(self, attribute_name):
            out = []
            for n_thing in getattr(self, attribute_name):
                out.append(n_thing)
            return out
        else:
            raise ValueError("this instance does not have the attribute {}".format(attribute_name))

    def _get_simple_property(self, property_name):
        if hasattr(self, property_name):
            return getattr(self, property_name)

    def _set_a_list_property(self, x, property_name, list_item_class):
        if isinstance(x, list):
            tally = 0
            for n_col in x:
                if isinstance(list_item_class, list):
                    passed = []
                    for n_potential_type in list_item_class:
                        if isinstance(n_col, n_potential_type):
                            passed.append(True)
                        else:
                            passed.append(False)
                    if True not in passed:
                        raise ValueError("item {} in inputted list is not a valid type for that list.".format(str(tally)))
                else:
                    if not isinstance(n_col, list_item_class):
                        raise ValueError("item {} in inputted list is not an instance of {}".format(str(tally), list_item_class))
                tally += 1
            setattr(self, property_name, x)
        else:
            raise ValueError("parameter passed to {} must be a list".format(property_name))
    
    def _set_numeric_property(self, x, property_name):
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

        :param url a string representing a live web resource

        :rtype bool
        :return a boolean that asseses whether or not the url is a valid URI

        taken from https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except:
            return False

    def _check_if_url_is_alive(self, url):
        """a method to check if url is alive

        :param url a string representing a live web resource

        :rtype bool
        :return a boolean that asseses whether or not the url given is resolvable

        taken from  https://stackoverflow.com/questions/16778435/python-check-if-website-exists
        """
        response = requests.get(url, "HEAD")
        if not self._check_if_url_valid(url):
            return False
        if (response.status_code == 404) or (response.status_code < 400):
            return True
        else:
            return False

    def get_type(self):
        return self._type

    def set_type(self, x):
        if x in valid_types:
            self._type = x
        else:
            raise ValueError("{} is not a valid type for a IIIF record".format(x))

    def del_type(self, x):
        self._type = None

    def get_id(self):
        return self._id

    def set_id(self, x):
        if self._check_if_url_valid(x):
            self._id = x
        else:
            raise ValueError("{} is not a valid url".format(x))

    def del_id(self):
        if self._id:
            self._id = None

    def get_context(self):
        return self._context

    def set_context(self, x):
        if not hasattr(self, '_context'):
            self._context = valid_contexts[0]
        else:
            raise ValueError("there is already a context set on this instance")

    def del_context(self):
        if self._viewingHint:
            self._viewingHint = None

    def get_viewingHint(self):
        return self._viewingHint

    def set_viewingHint(self, x):
        if x in valid_viewingHints:
            self._viewingHint = x
        else:
            raise ValueError("{} is not a valid viewingHint".format(x))

    def del_viewingHint(self):
        if self._viewingHint:
            self._viewingHint = None

    def get_viewingDirection(self):
        return self._viewingDirection

    def set_viewingDirection(self, x):
        if x in valid_viewingDirections:
            self._viewingDirection = x
        else:
            raise ValueError("{} is not a valid viewingDirection".format(x))

    def del_viewingDirection(self):
        if self._viewingDirection:
            self._viewingDirection = None

    def get_label(self):
        return self._label

    def set_label(self, x):
        self._label = x

    def del_label(self):
        if self._label:
            self._label = None

    def get_description(self):
        return self._description

    def set_description(self, x):
        self._description = x

    def del_description(self):
        if self._description:
            self._description = None

    def load(self, json_data):
        """load data from a json record

        takes a stringified JSON record and loads it into an instance of Record

        :param json_data a string that can be loaded into a python dictionary

        :rtype None
        :return None
        """
        json_data = json.loads(json_data)
        if isinstance(json_data, dict):
            self.id = json_data.get("@id")
            self.type = json_data.get("@type")
            if json_data.get("@context"):
                self.context = json_data.get("@context")
            if json_data.get("label"):
                self.label = json_data.get("label")
            if json_data.get("viewingHint"):
                self.viewingHint = json_data.get("viewingHint")
            if json_data.get("viewingDirection"):
                self.viewingDirection = json_data.get("viewingDirection")
        else:
            raise ValueError("JSON string loaded must convert to a dictionary")

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


    type = property(get_type, set_type, del_type)
    id = property(get_id, set_id, del_id)
    context = property(get_context, set_context, del_context)
    viewingHint = property(get_viewingHint, set_viewingHint, del_viewingHint)
    viewingDirection = property(get_viewingDirection, set_viewingDirection, del_viewingDirection)
    label = property(get_label, set_label, del_label)
    description = property(get_description, set_description, del_description)


class Collection(Record):
    """a class for building IIIF Collection records

    :rtype Collection
    :return an instance of a Colllection record
    """

    def __init__(self, uri):
        """"initializes a Collection with type sc:Collection and id of uri given at init
        """
        self.context = "foo"
        self.type = "sc:Collection"
        self.id = uri

    def __repr__(self):
        return "<IIF Collection record for {} >".format(self.id)

    def get_collections(self):
        return self._iterate_some_list('_collections')

    def set_collections(self, x):
        self._set_a_list_property(x, '_collections', Collection)

    def del_collections(self):
        if hasattr(self, "_collections"):
            self._collections = None

    def get_manifests(self):
        return self._iterate_some_list('_manifests')

    def set_manifests(self, x):
        self._set_a_list_property(x, '_manifests', Manifest)

    def del_manifests(self):
        self._delete_a_property("_manifests")

    def get_members(self):
        return self._iterate_some_list('_members')

    def set_members(self, x):
        self._set_a_list_property(x, '_manifests', [Manifest, Collection])

    def del_members(self):
        if hasattr(self, "_members"):
            self._manifests = None
        else:
            raise ValueError("members hasn't been set on this instance")

    collections = property(get_collections, set_collections, del_collections)
    manifests = property(get_manifests, set_manifests, del_manifests)
    members = property(get_members, set_members, del_members)


class Manifest(Record):
    def __init__(self, uri):
        self.context = "foo"
        self.type = "sc:Manifest"
        self.id = uri

    def get_sequences(self):
        return self._iterate_some_list("_sequences")

    def set_sequences(self, x):
        self._set_a_list_property(x, "_sequences", Sequence)
        pass

    def del_sequences(self):
        self._delete_a_property("_structures")

    def get_structures(self):
        return self._iterate_some_list("_structures")

    def set_structures(self, x):
        self._set_a_list_property(x, "_structures", Range)

    def del_structures(self):
        self._delete_a_property("_structures")

    sequences = property(get_sequences, set_sequences, del_sequences)
    structures = property(get_structures, set_structures, del_structures)


class Sequence(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:Sequence"
        self.canvases = []

    def get_canvases(self):
        return self._iterate_some_list("_canvases")

    def set_canvases(self, x):
        self._set_a_list_property(x, "_canvases", Canvas)

    def del_canvases(self):
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

    canvases = property(get_canvases, set_canvases, del_canvases)


class Canvas(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:Canvas"

    def get_images(self):
        return self._iterate_some_list("_images")

    def set_images(self, x):
        self._set_a_list_property(x, "_canvases", Annotation)

    def del_images(self):
        self._delete_a_property("_images")

    def get_otherContent(self):
        return self._iterate_some_list("_otherContent")

    def set_otherContent(self, x):
        self._set_a_list_property(x, "_otherContent", AnnotationList)

    def del_otherContent(self):
        self._delete_a_property("_otherContent")

    def get_height(self):
        return self._get_simple_property("_height")

    def set_height(self, x):
        self._set_numeric_property(x, "_height")

    def del_height(self):
        self._delete_a_property("_height")

    def get_width(self):
        return self._get_simple_property("_width")

    def set_width(self, x):
        self._set_numeric_property(x, "_width")

    def del_width(self):
        self._delete_a_property("_width")

    def validate(self):
        if hasattr(self, 'height') and hasattr(self, 'width') and hasattr(self, 'label') and hasattr(self, 'images'):
            return True
        else:
            return False

    images = property(get_images, set_images, del_images)
    height = property(get_height, set_height, del_height)
    width = property(get_height, set_height, del_height)
    otherContent = property(get_otherContent, set_otherContent, del_otherContent)

class AnnotationList(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:AnnotationList"

    def get_resources(self):
        return self._iterate_some_list("_resources")

    def set_resources(self, x):
        return self._set_a_list_property(x, "_resources", Annotation)

    def del_resources(self):
        self._delete_a_property("_resources")

    resources = property(get_resources, set_resources, del_resources)

class Annotation(Record):
    def __init__(self):
        pass


class ImageContent(Record):
    def __init__(self):
        pass

    def get_format(self):
        pass

    def set_format(self):
        pass

    def del_format(self):
        pass

    format = property(get_format, set_format, del_format)


class OtherContent(Record):
    def __init__(self):
        pass

    def get_format(self):
        pass

    def set_format(self):
        pass

    def del_format(self):
        pass

    format = property(get_format, set_format, del_format)

class Range(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:Range"
        
    def get_canvases(self):
        return self._iterate_some_list("_canvases")

    def set_canvases(self, x):
        return self._set_a_list_property(x, "_canvases", Canvas)

    def del_canvases(self):
        self._delete_a_property("_canvases")

    def get_members(self):
        return self._iterate_some_list("_members")

    def set_members(self, x):
        return self._set_a_list_property(x, "_members", [Canvas, Range])

    def del_members(self):
        self._delete_a_property("_members")

    def get_ranges(self):
        return self._iterate_some_list("_ranges")

    def set_ranges(self, x):
        return self._set_a_list_property(x, "_ranges", Range)

    def del_ranges(self):
        self._delete_a_property("_ranges")

    canvases = property(get_canvases, set_canvases, del_canvases)
    members = property(get_members, set_members, del_members)
    ranges = property(get_ranges, set_ranges, del_ranges)

# JSON-LD @types to Class
ttc = {
    "sc:Collection": Collection,
    "sc:Manifest": Manifest,
    "sc:Sequence": Sequence,
    "sc:Canvas": Canvas,
    "oa:Annotation": Annotation,
    "sc:AnnotationList": AnnotationList,
    "sc:Range": Range,
    "dctypes:Image": ImageContent
}
