import json


class Record:
    """
    Record interface brainstorming
    """
    def __init__(self, *args, **kwargs):
        raise NotImplemented()

    def dumps(self, **kwargs):
        """
        Dumps the record to a string representation.

        :rtype: str
        :returns: A JSON representation of the record
        """
        return json.dumps(self.j, **kwargs)

    def dump(self, flo, **kwargs):
        """
        Dumps the record to a file like object

        :param file_like_object flo: The file like object to write the
            representation to

        :rtype: None
        """
        return json.dump(self.j, flo, **kwargs)

    def get_type(self):
        return self.j.get('@type')

    def set_type(self, x):
        self.j['@type'] = x

    def del_type(self, x):
        self.j['@type'] = None

    def get_id(self):
        return self.j.get('@id')

    def set_id(self, x):
        self.j['@id'] = x

    def del_id(self):
        del self.j['@id']

    @classmethod
    def load(cls, *args, **kwargs):
        """
        Load a record from a file like object

        See :func:`json.load`
        """
        j = json.load(*args, **kwargs)
        cls._validate(j)
        return cls()

    @classmethod
    def loads(cls, *args, **kwargs):
        """
        Load a record from a string

        See :func:`json.loads`
        """
        j = json.loads(*args, **kwargs)
        cls._validate(j)
        return cls()

    @classmethod
    def validate(self):
        """
        Validate this record

        :rtype: bool
        """
        try:
            self._validate(self.j)
            return True
        except Exception:
            return False

    @staticmethod
    def _validate(x):
        """
        validate JSON as a record

        :rtype: None
        """
        raise NotImplemented()

    type = property(get_type, set_type, del_type)
    id = property(get_id, set_id, del_id)


class Collection(Record):
    def __init__(self):
        pass

    def get_collections(self):
        pass

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
    def __init__(self):
        pass

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


class Range(Record):
    def __init__(self):
        pass

    def get_members(self):
        pass

    def set_members(self):
        pass

    def del_members(self):
        pass

    def get_canvases(self):
        pass

    def set_canvases(self):
        pass

    def del_canvases(self):
        pass

    memebers = property(get_members, set_members, del_members)
    canvases = property(get_canvases, set_canvases, del_canvases)


class Layer(Record):
    def __init__(self):
        pass

    def get_otherContent(self):
        pass

    def set_otherContent(self):
        pass

    def del_otherContent(self):
        pass

    otherContent = property(get_otherContent, set_otherContent, del_otherContent)


class AnnotationList(Record):
    def __init__(self):
        pass

    def get_resources(self):
        pass

    def set_resources(self):
        pass

    def del_resources(self):
        pass

    resources = property(get_resources, set_resources, del_resources)


class Sequence(Record):
    def __init__(self):
        pass

    def get_canvases(self):
        pass

    def set_canvases(self):
        pass

    def del_canvases(self):
        pass

    canvases = property(get_canvases, set_canvases, del_canvases)


class Canvas(Record):
    def __init__(self):
        pass

    def get_images(self):
        pass

    def set_images(self):
        pass

    def del_images(self):
        pass

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
    "sc:Range": Range,
    "sc:Layer": Layer,
    "sc:AnnotationList": AnnotationList,
    "sc:Sequence": Sequence,
    "sc:Canvas": Canvas,
    "oa:Annotation": Annotation,
    "dctypes:Image": ImageContent
}
