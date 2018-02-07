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


class Collection(Record):
    pass


class Manifest(Record):
    pass


class Range(Record):
    pass


class Layer(Record):
    pass


class AnnotationList(Record):
    pass


class Sequence(Record):
    pass


class Canvas(Record):
    pass


class Annotation(Record):
    pass


class Content(Record):
    pass


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
    "dctypes:Image": Content
}
