"""Test module for pyiiif twodotone compliance 
"""

import json
import pytest
import unittest

import pyiiif
from pyiiif.pres_api.twodotone.records import Record, Collection, Manifest, Sequence


class Tests(unittest.TestCase):
    def setUp(self):
        # Perform any setup that should occur
        # before every test
        pass

    def tearDown(self):
        # Perform any tear down that should
        # occur after every test
        pass

    def testPass(self):
        self.assertEqual(True, True)

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

    def testMixOfRecords(self):
        collection = Collection("https://www.lib.uchicago.edu/collex/?digital=on&view=collections")
        manifest = Manifest("https://www2.lib.uchicago.edu/")
        sequence = Sequence("https://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")
        return self.assertEquals(collection.type, "sc:Collection") and \
               self.assertEquals(collection.id, "https://www.lib.uchicago.edu/collex/?digital=on&view=collections") and \
               self.assertEquals(manifest.type, "sc:Manifest") and \
               self.assertEquals(manifest.id, "https://www2.lib.uchicago.edu/") and \
               self.assertEquals(sequence.type, "sc:Sequence") and \
               self.assertEquals(sequence.id, "https://www.lib.uchicago.edu/about/directory/?view=staff&subject=All+Subject+Specialists")

if __name__ == "__main__":
    unittest.main()
