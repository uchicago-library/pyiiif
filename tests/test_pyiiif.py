"""Test module for pyiiif twodotone compliance 
"""

import json
import pytest
import unittest

import pyiiif
from pyiiif.pres_api.twodotone.records import Annotation, Record, Collection, Manifest, \
    Sequence, Canvas, AnnotationList, Range, ImageResource


class Tests(unittest.TestCase):
    def setUp(self):
        # Perform any setup that should occur
        # before every test
        pass

    def tearDown(self):
        # Perform any tear down that should
        # occur after every test
        pass

    def testVersionAvailable(self):
        x = getattr(pyiiif, "__version__", None)
        self.assertTrue(x is not None)

    def testBuildGenericRecord(self):
        x = Record()
        x.id = "http://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        self.assertEqual(x.type, "sc:Collection") and \
                        (x.id,
                         "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/")

    def testBuildFullerRecord(self):
        x = Record()
        x.id = "http://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        x.viewingDirection = "left-to-right"
        x.viewingHint = "individuals"
        x.label = "An Example Collection"
        x.description = "This is a test collection"
        self.assertEqual(x.type, "sc:Collection") and \
                        self.assertEqual(x.id,
                         "http://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/") and \
                        self.assertEqual(x.viewingDirection, "individuals") and \
                        self.assertEqual(x.label, "An Example Collectoin") and \
                        self.assertEqual(x.description, "This is a test collection")

    def testGetStringOfInput(self):
        x = Record()
        x.id = "http://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        x.viewingDirection = "left-to-right"
        x.viewingHint = "individuals"
        x.label = "An Example Collection"
        x.description = "This is a test collection"
        stringified = str(x)
        a_dict = json.loads(stringified)
        return self.assertEqual(a_dict.get("@type"), x.type) and \
               self.assertEqual(a_dict.get("@id"), x.id) and \
               self.assertEqual(a_dict.get("viewingDirection"), x.viewingDirection) and \
               self.assertEqual(a_dict.get("viewingHint"), x.viewingHint) and \
               self.assertEqual(a_dict.get("description"), x.description) and \
               self.assertEqual(a_dict.get("label"), x.label)

    def testLoadFromString(self):
        input_string = '{"@type": "sc:Manifest", "label": "Test", "description": "A test", "@id": "https://www.lib.uchicago.edu/", "viewingHint": "individuals", "viewingDirection": "left-to-right", "@context": "https://iiif.io/api/presentation/2/context.json"}'
        x = Manifest.load(input_string)
        return self.assertEqual(x.type, "sc:Manifest") and \
               self.assertEqual(x.id, "http://www2.lib.uchicago.edu/") and \
               self.assertEqual(x.context, "https://iiif.io/api/presentation/2/context.json") and \
               self.assertEqual(x.viewingDirection, "left-to-right") and \
               self.assertEqual(x.viewingHint, "individuals") and \
               self.assertEqual(x.description, "A test") and \
               self.assertEqual(x.label, "Test")

    def testLoadFromStringWithMetadata(self):
        input_dict = {"@type": "sc:Manifest", "label": "Test", 
                      "description": "A test", 
                      "@id": "https://www.lib.uchicago.edu/", 
                      "metadata": [
                          {"label": "A Test Label", "value": "A test value"}
                      ],
                      "viewingHint": "individuals",
                      "viewingDirection": "left-to-right",
                      "@context": "https://iiif.io/api/presentation/2/context.json"}
        x = Manifest.load(json.dumps(input_dict))
        metadata = x.metadata
        return self.assertEqual(metadata[0].label.lower(), 'a test label')

    def testLoadFromStringAndGetBackSameInToDict(self):
        input_dict = {"@type": "sc:Manifest", "label": "Test", 
                      "description": "A test", 
                      "@id": "https://www.lib.uchicago.edu/", 
                      "metadata": [
                          {"label": "A Test Label", "value": "A test value"}
                      ],
                      "viewingHint": "individuals",
                      "viewingDirection": "left-to-right",
                      "@context": "https://iiif.io/api/presentation/2/context.json"}
        x = Manifest.load(json.dumps(input_dict))
        converted = x.to_dict()
        metadata = x.metadata
        print(converted.get("metadata"))
        return self.assertNotEqual(converted.get("metadata"), None) and \
               self.assertEqual(converted.get("metadata")[0]["label"].lower(), "a test label") and \
               self.assertEqual(converted.get("viewingHint") , "individuals") and \
               self.assertEqual(converted.get("@context"), "https://iiif.io/api/presentation/2/context.json")

    def testValidateGoodRecordReturnsTrue(self):
        x = Record()
        x.id = "http://www2.lib.uchicago.edu/"
        x.type = "sc:Manifest"
        check = x.validate()
        return self.assertEqual(check[0], True) and self.assertEqual(check[1], [])
 
    def testValidateBadRecordReturnsFalse(self):
        new = Record()
        new.id = "http://www2.lib.uchicago.edu/"
        check = new.validate()
        return self.assertEqual(check[0], False) and \
               self.assertEqual(check[1], ["A IIIF record must have a valid type attribute"])
 
    def testBadViewingDirectionInput(self):
        x = Record()
        with pytest.raises(ValueError):
            x.viewingDirection = "foo"

    def testBadViewingHintInput(self):
        x = Record()
        with pytest.raises(ValueError):
            x.viewingHint = "foo"

    def testInvalidID(self):
        x = Record()
        with pytest.raises(ValueError):
            x.id = "foo"

    def testInvalidType(self):
        x = Record()
        with pytest.raises(ValueError):
            x.type = "foo"

    def testMultipleRecords(self):
        x1 = Record()
        x1.id = "http://lib.uchicago.edu/"
        x1.type = "sc:Manifest"
        x2 = Record()
        x2.id = "http://www.lib.uchicago.edu/collex/?digital=on&view=collections"
        x2.type = "sc:Collection"
        return self.assertEqual(x1.id, "http://lib.uchicago.edu/") and \
               self.assertEqual(x2.id, "http://www.lib.uchicago.edu/collex/?digital=on&view=collections")

    def testBuildMixOfRecords(self):
        collection = Collection("http://www.lib.uchicago.edu/collex/?digital=on&view=collections")
        manifest = Manifest("http://www2.lib.uchicago.edu/")
        sequence = Sequence("http://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")
        return self.assertEqual(collection.type, "sc:Collection") and \
               self.assertEqual(collection.id, "http://www.lib.uchicago.edu/collex/?digital=on&view=collections") and \
               self.assertEqual(manifest.type, "sc:Manifest") and \
               self.assertEqual(manifest.id, "http://www2.lib.uchicago.edu/") and \
               self.assertEqual(sequence.type, "sc:Sequence") and \
               self.assertEqual(sequence.id, "http://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")

    def testBuildManifestWithASequence(self):
        m = Manifest("http://lib.uchicago.edu/")
        s = Sequence("http://lib.uchicago.edu/")
        s.canvases = [Canvas("http://lib.uchicago.edu/")]
        m.sequences = [s]
        return self.assertEqual(str(m.sequences), "[Sequence for http://lib.uchicago.edu/]") and \
               self.assertEqual(m.id, 'http://lib.uchicago.edu/')
    
    def testBuildCollectionWithMembers(self):
        c = Collection("http://lib.uchicago.edu/")
        c.members = [Manifest("http://lib.uchicago.edu/")]
        return self.assertEqual(str(c.members), "[Manifest for http://lib.uchicago.edu/]") and \
               self.assertEqual(c.id, 'http://lib.uchicago.edu/')

    def testBuildCanvas(self):
        c = Canvas("http://lib.uchicago.edu/")
        c.height = 1000
        c.width = 500
        return self.assertEqual(c.height, 1000) and \
               self.assertEqual(c.width, 500) and \
               self.assertEqual(c.id, "http://lib.uchicago.edu/")

    def testBuildSequence(self):
        s = Sequence("http://lib.uchicago.edu/")
        s.canvases = [Canvas("http://lib.uchicago.edu/")]
        return self.assertEqual(str(s.canvases), "[Canvas for http://lib.uchicago.edu/]") and \
               self.assertEqual(s.id, 'http://lib.uchicago.edu/')

    def testBuildAnnotationList(self):
        s = AnnotationList("http://lib.uchicago.edu/")
        s.canvases = [Annotation("http://lib.uchicago.edu/", "https://example/org/bar")]
        return self.assertEqual(str(s.canvases), "[Annotation for http://lib.uchicago.edu/]") and \
               self.assertEqual(s.id, 'http://lib.uchicago.edu/') 

    def testGetCanvasDict(self):
        canvas = Canvas("http://lib.uchicago.edu/canvas")
        canvas.height = 1000
        canvas.width = 509
        canvas.label = "A Canvas"
        canvas.description = "This a IIIF Canvas created programatically"
        annotation = Annotation("http://lib.uchicago.edu/annotation", "https://example.org/bar")
        an_image = ImageResource('https', 'iiif-server.lib.uchicago.edu', '', 'default-photo.original.jpg', 'image/jpeg')
        an_image.set_width(1)
        an_image.set_height(1)
        annotation.resource = an_image
        canvas.images = [annotation]
        return self.assertEqual(canvas.to_dict()["images"][0]["resource"]["@id"], "https://iiif-server.lib.uchicago.edu/default-photo.original.jpg/full/full/0/default.jpg") and \
               self.assertEqual(canvas.to_dict()["images"][0]["resource"]["format"], "image/jpeg")

    def testGetManifestDict(self):
        manifest = Manifest("http://lib.uchicago.edu/manifest")
        manifest.viewingHint = "individuals"
        manifest.viewingDirection = "left-to-right"
        sequence = Sequence("http://lib.uchicago.edu/sequence")
        canvas = Canvas("http://lib.uchicago.edu/canvas")
        canvas.height = 1000
        canvas.width = 509
        canvas.label = "A Canvas"
        canvas.description = "This a IIIF Canvas created programatically"
        annotation = Annotation("http://lib.uchicago.edu/annotation", "https://example.org/bar")
        an_image = ImageResource('https', 'iiif-server.lib.uchicago.edu', '', 'default-photo.original.jpg', 'image/jpeg')
        an_image.set_width(1)
        an_image.set_height(1)
        annotation.resource = an_image
        canvas.images = [annotation]
        sequence.canvases = [canvas]
        manifest.sequences = [sequence]
        return self.assertEqual(len(manifest.to_dict()["sequences"]), 1) and \
               self.assertEqual(manifest.to_dict()["viewingHint"] == "individuals")

if __name__ == "__main__":
    unittest.main()
