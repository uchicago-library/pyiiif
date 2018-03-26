
from pyiiif.pres_api.twodotone.records import Collection, Record, ImageResource, Canvas, Sequence, Manifest
import json

out = {}
out["@id"] = "http://lib.uchicago.edu/manifest"
out["@type"] = "sc:Manifest"
out["@context"] = "http://iiif.io/api/presentation/2/context.json"
out["label"] = "A Label"
out["description"] = "This is a description"
out["sequences"] = []
a_seq = {}
a_seq["@id"] = "http://lib.uchicago.edu/sequence/1"
a_seq["@type"] = "sc:Sequence"
out["viewingHint"] = "individuals"
out["viewingDirection"] = "left-to-right"
a_seq["canvases"] = []
a_canvas = {}
a_canvas["@id"] = "http://lib.uchicago.edu/canvas/1"
a_canvas["@type"] = "sc:Canvas"
a_canvas["label"] = "A Canvas"
a_canvas["images"] = []
a_canvas["height"] = 1000
a_canvas["width"] = 500
an_annotation = {}
an_annotation["@id"] = "http://lib.uchicago.edu/annotation/1"
an_annotation["@context"] = "http://iiif.io/api/presentation/2/context.json"
an_annotation["@type"] = "oa:Annotation"
an_annotation["motivation"] = "sc:Painting"
an_annotation["resource"] = {}

img_resource = {}
img_resource["@id"] = "http://iiif-server.lib.uchicago.edu/default-photo.original.jpg/full/full/0/default.jpg"
img_resource["service"] = {"@id": "http://iiif-server.lib.uchicago.edu/default-photo.original.jpg", "@context": "https://iiif.io/image/2/level2.json"}
img_resource["@type"] = "dctypes:Image"
an_annotation["resource"] = img_resource
a_canvas["images"] = [an_annotation]
a_seq["canvases"] = [a_canvas]
out["sequences"] = [a_seq]

# testing loading image resource
imgresource_string = json.dumps(img_resource)
i = ImageResource.load(imgresource_string)

# testing loading canvas
canvas_string = json.dumps(a_canvas)
c = Canvas.load(canvas_string)
print(c)

# testing loading sequence
sequence_string = json.dumps(a_seq)
s = Sequence.load(sequence_string)
print(s)

# testing loading manifest
manifest_string = json.dumps(out)
m = Manifest.load(manifest_string)
print(m.sequences)
for s in m.sequences:
    print(s.canvases)
    for canvas in s.canvases:
        print(canvas.images)
        for anno in canvas.images:
            print(anno.resource)