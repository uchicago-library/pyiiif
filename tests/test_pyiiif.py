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
        x.id = "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        self.assertEqual(x.type, "sc:Collection") and \
                        (x.id,
                         "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/")

    def testBuildFullerRecord(self):
        x = Record()
        x.id = "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        x.viewingDirection = "left-to-right"
        x.viewingHint = "individuals"
        x.label = "An Example Collection"
        x.description = "This is a test collection"
        self.assertEqual(x.type, "sc:Collection") and \
                        self.assertEquals(x.id,
                         "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/") and \
                        self.assertEquals(x.viewingDirection, "individuals") and \
                        self.assertEquals(x.label, "An Example Collectoin") and \
                        self.assertEquals(x.description, "This is a test collection")

    def testGetStringOfInput(self):
        x = Record()
        x.id = "https://www.lib.uchicago.edu/collex/collections/archicofrad-del-santsimo-sacramento-y-caridad-records/"
        x.type = "sc:Collection"
        x.viewingDirection = "left-to-right"
        x.viewingHint = "individuals"
        x.label = "An Example Collection"
        x.description = "This is a test collection"
        stringified = str(x)
        a_dict = json.loads(stringified)
        return self.assertEquals(a_dict.get("@type"), x.type) and \
               self.assertEquals(a_dict.get("@id"), x.id) and \
               self.assertEquals(a_dict.get("viewingDirection"), x.viewingDirection) and \
               self.assertEquals(a_dict.get("viewingHint"), x.viewingHint) and \
               self.assertEquals(a_dict.get("description"), x.description) and \
               self.assertEquals(a_dict.get("label"), x.label)

    def testLoadFromString(self):
        input_string = '{"@type": "sc:Manifest", "label": "Test", "description": "A test", "@id": "https://www.lib.uchicago.edu/", "viewingHint": "individuals", "viewingDirection": "left-to-right", "@context": "https://iiif.io/api/presentation/2/context.json"}'
        x = Record()
        x.load(input_string)
        return self.assertEquals(x.type, "sc:Manifest") and \
               self.assertEquals(x.id, "https://www2.lib.uchicago.edu/") and \
               self.assertEquals(x.context, "https://iiif.io/api/presentation/2/context.json") and \
               self.assertEquals(x.viewingDirection, "left-to-right") and \
               self.assertEquals(x.viewingHint, "individuals") and \
               self.assertEquals(x.description, "A test") and \
               self.assertEquals(x.label, "Test")

    def testValidateGoodRecordReturnsTrue(self):
        x = Record()
        x.id = "https://www2.lib.uchicago.edu/"
        x.type = "sc:Manifest"
        check = x.validate()
        return self.assertEquals(check[0], True) and self.assertEquals(check[1], [])
 
    def testValidateBadRecordReturnsFalse(self):
        new = Record()
        new.id = "https://www2.lib.uchicago.edu/"
        check = new.validate()
        return self.assertEquals(check[0], False) and \
               self.assertEquals(check[1], ["A IIIF record must have a valid type attribute"])
 
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
        x1.id = "https://lib.uchicago.edu/"
        x1.type = "sc:Manifest"
        x2 = Record()
        x2.id = "https://www.lib.uchicago.edu/collex/?digital=on&view=collections"
        x2.type = "sc:Collection"
        return self.assertEquals(x1.id, "https://lib.uchicago.edu/") and \
               self.assertEquals(x2.id, "https://www.lib.uchicago.edu/collex/?digital=on&view=collections")

    def testBuildMixOfRecords(self):
        collection = Collection("https://www.lib.uchicago.edu/collex/?digital=on&view=collections")
        manifest = Manifest("https://www2.lib.uchicago.edu/")
        sequence = Sequence("https://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")
        return self.assertEquals(collection.type, "sc:Collection") and \
               self.assertEquals(collection.id, "https://www.lib.uchicago.edu/collex/?digital=on&view=collections") and \
               self.assertEquals(manifest.type, "sc:Manifest") and \
               self.assertEquals(manifest.id, "https://www2.lib.uchicago.edu/") and \
               self.assertEquals(sequence.type, "sc:Sequence") and \
               self.assertEquals(sequence.id, "https://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")

    def testBuildManifestWithASequence(self):
        m = Manifest("https://lib.uchicago.edu/")
        s = Sequence("https://lib.uchicago.edu/")
        s.canvases = [Canvas("https://lib.uchicago.edu/")]
        m.sequences = [s]
        return self.assertEquals(str(m.sequences), "[Sequence for https://lib.uchicago.edu/]") and \
               self.assertEquals(m.id, 'https://lib.uchicago.edu/')
    
    def testBuildCollectionWithMembers(self):
        c = Collection("https://lib.uchicago.edu/")
        c.members = [Manifest("https://lib.uchicago.edu/")]
        return self.assertEquals(str(c.members), "[Manifest for https://lib.uchicago.edu/]") and \
               self.assertEquals(c.id, 'https://lib.uchicago.edu/')

    def testBuildCanvas(self):
        c = Canvas("https://lib.uchicago.edu/")
        c.height = 1000
        c.width = 500
        return self.assertEquals(c.height, 1000) and \
               self.assertEquals(c.width, 500) and \
               self.assertEquals(c.id, "https://lib.uchicago.edu/")

    def testBuildSequence(self):
        s = Sequence("https://lib.uchicago.edu/")
        s.canvases = [Canvas("https://lib.uchicago.edu/")]
        return self.assertEquals(str(s.canvases), "[Canvas for https://lib.uchicago.edu/]") and \
               self.assertEquals(s.id, 'https://lib.uchicago.edu/')

    def testBuildAnnotationList(self):
        s = AnnotationList("https://lib.uchicago.edu/")
        s.canvases = [Annotation("https://lib.uchicago.edu/")]
        return self.assertEquals(str(s.canvases), "[Annotation for https://lib.uchicago.edu/]") and \
               self.assertEquals(s.id, 'https://lib.uchicago.edu/') 

    def testGetCanvasDict(self):
        canvas = Canvas("https://lib.uchicago.edu/canvas")
        canvas.height = 1000
        canvas.width = 509
        canvas.label = "A Canvas"
        canvas.description = "This a IIIF Canvas created programatically"
        annotation = Annotation("https://lib.uchicago.edu/annotation")
        an_image = ImageResource("https://iiif-server.lib.uchicago.edu/default-photo.original.jpg", "image/jpeg")
        annotation.resource = an_image
        canvas.images = [annotation]
        print(canvas.to_dict())
        return self.assertEquals(canvas.to_dict()["images"][0]["resource"]["@id"], "https://iiif-server.lib.uchicago.edu/default-photo.original.jpg/full/full/0/default.jpg") and \
               self.assertEquals(canvas.to_dict()["images"][0]["resource"]["format"], "image/jpeg")

    def testGetManifestDict(self):
        manifest = Manifest("http://lib.uchicago.edu/manifest")
        manifest.viewingHint = "individuals"
        manifest.viewingDirection = "left-to-right"
        sequence = Sequence("https://lib.uchicago.edu/sequence")
        canvas = Canvas("https://lib.uchicago.edu/canvas")
        canvas.height = 1000
        canvas.width = 509
        canvas.label = "A Canvas"
        canvas.description = "This a IIIF Canvas created programatically"
        annotation = Annotation("https://lib.uchicago.edu/annotation")
        an_image = ImageResource("https://iiif-server.lib.uchicago.edu/default-photo.original.jpg", "image/jpeg")
        annotation.resource = an_image
        canvas.images = [annotation]
        sequence.canvases = [canvas]
        manifest.sequences = [sequence]
        return self.assertEquals(len(manifest.to_dict()["sequences"]), 1) and \
               self.assertEquals(manifest.to_dict()["viewingHint"] == "individuals")

if __name__ == "__main__":
    unittest.main()
