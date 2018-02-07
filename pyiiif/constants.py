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
