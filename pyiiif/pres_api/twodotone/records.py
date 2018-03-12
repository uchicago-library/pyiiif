import json
import requests
from urllib.parse import urlparse

_valid_viewingHints = ["individuals",
                       "paged",
                       "continuous",
                       "multi-part",
                       "non-paged",
                       "top",
                       "facing-pages"
                       ]
_valid_viewingDirections = ["left-to-right",
                            "right-to-left",
                            "top-to-bottom",
                            "bottom-to-top"
                           ]
_valid_types = ["sc:Manifest",
                "sc:Sequence",
                "sc:Canvas",
                "sc:Content",
                "sc:Collection",
                "sc:Annotation",
                "sc:AnnotationList",
                "sc:Range",
                "sc:Layer"
               ]
_valid_contexts = ["https://iiif.io/api/presentations/2/context.json"]



class Record:
    """
    Record interface brainstorming
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
        
    def _check_if_url_valid(self, url):
        """a method to check if an input url is well-formed or not

        taken from https://stackoverflow.com/questions/7160737/python-how-to-validate-a-url-in-python-malformed-or-not/7160778
        """
        try:
            result = urlparse(url)
            return result.scheme and result.netloc and result.path
        except:
            return False

    def _check_if_url_is_alive(self, url):
        """a method to check if url is alive

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
        if x in _valid_types:
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
            self._context = _valid_contexts[0]
        else:
            raise ValueError("there is already a context set on this instance")

    def del_context(self):
        if self._viewingHint:
            self._viewingHint = None

    def get_viewingHint(self):
        return self._viewingHint

    def set_viewingHint(self, x):
        if x in _valid_viewingHints:
            self._viewingHint = x
        else:
            raise ValueError("{} is not a valid viewingHint".format(x))

    def del_viewingHint(self):
        if self._viewingHint:
            self._viewingHint = None

    def get_viewingDirection(self):
        return self._viewingDirection

    def set_viewingDirection(self, x):
        if x in _valid_viewingDirections:
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
        if (getattr(self, "viewingDirection", None)) and (getattr(self, "viewingDirection", None) not in _valid_viewingDirections):
            errors.append("If viewingDirection is present on a IIIF record it must be valid direction")
        if (getattr(self, "viewingHint", None)) and (getattr(self, "viewingHint", None) not in _valid_viewingHints):
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
    def __init__(self, uri):
        self.context = "foo"
        self.type = "sc:Collection"
        self.id = uri

    def get_collections(self):
        for n_coll in self.members:
            return n_coll

    def set_collections(self):
        pass

    def del_collections(self):
        pass

    def get_manifests(self):
        pass

    def set_manifests(self):
        pass

    def del_manifests(self):
        pass

    def get_members(self):
        pass

    def set_members(self):
        pass

    def del_members(self):
        pass

    collections = property(get_collections, set_collections, del_collections)
    manifests = property(get_manifests, set_manifests, del_manifests)
    members = property(get_members, set_members, del_members)


class Manifest(Record):
    def __init__(self, uri):
        self.context = "foo"
        self.type = "sc:Manifest"
        self.id = uri

    def get_sequences(self):
        pass

    def set_sequences(self):
        pass

    def del_sequences(self):
        pass

    def get_structures(self):
        pass

    def set_structures(self):
        pass

    def del_structures(self):
        pass

    sequences = property(get_sequences, set_sequences, del_sequences)
    structures = property(get_structures, set_structures, del_structures)


class Sequence(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:Sequence"
        self.canvases = []

    def get_canvases(self):
        """a method to get the canvases available in a sequence. 

        :rtype list
        :returns a list of the identifiers for the canvases associated
        with the sequence
        """
        output = []
        for n_canvas in self.canvases:
            output.append(n_canvas.get("id"))
        return output

    def set_canvases(self, x):
        self._canvases = x 

    def del_canvases(self):
        self._canvases = None

    def del_canvas(self, a_canvas):
        """a method to delete a canvas from a sequence

        takes a canvas object, checks if that object exists in the sequence
        and if it does deletes it from the list.

        :rtype bool
        :returns a Boolean value whether or not anything was deleted
        """
        output = None
        try:        
            pos_to_remove = self._canvases.index(a_canvas)
            self._canvases[pos_to_remove]
            output = True
        except ValueError:
            output = False
        return output

    canvases = property(get_canvases, set_canvases, del_canvases)


class Canvas(Record):
    def __init__(self, uri):
        self.id = uri
        self.type = "sc:Canvas"
        self.set_images()

    def get_images(self):
        pass

    def set_images(self):
        self.images = []

    def del_images(self):
        self.images = None

    def get_otherContent(self):
        pass

    def set_otherContent(self):
        pass

    def del_otherContent(self):
        pass

    images = property(get_images, set_images, del_images)
    otherContent = property(get_otherContent, set_otherContent, del_otherContent)


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


# JSON-LD @types to Class
ttc = {
    "sc:Collection": Collection,
    "sc:Manifest": Manifest,
    "sc:Sequence": Sequence,
    "sc:Canvas": Canvas,
    "oa:Annotation": Annotation,
    "dctypes:Image": ImageContent
}
