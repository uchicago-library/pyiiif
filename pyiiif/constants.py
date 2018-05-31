"""
Defines constants used by the rest of the module
"""


format_map = {
    "jpg": "JPEG",
    "tif": "TIFF",
    "png": "PNG",
    "gif": "GIF",
    "jp2": "JPEG2000",
    "pdf": "PDF",
    "webp": "WebP"
}

valid_image_formats = [k for k in format_map]

valid_schemes = [
    "http",
    "https"
]

valid_viewingHints = ["individuals",
                       "paged",
                       "continuous",
                       "multi-part",
                       "non-paged",
                       "top",
                       "facing-pages"
                       ]
valid_viewingDirections = ["left-to-right",
                            "right-to-left",
                            "top-to-bottom",
                            "bottom-to-top"
                           ]
valid_types = ["sc:Manifest",
               "sc:Sequence",
               "sc:Canvas",
               "sc:Content",
               "sc:Collection",
               "oa:Annotation",
               "sc:AnnotationList",
               "sc:Range",
               "sc:Layer",
               "dctypes:Image"
              ]

valid_contexts = {"presentation":"http://iiif.io/api/presentation/2/context.json",
                  "image": "http://iiif.io/api/image/2/context.json"
                 }

