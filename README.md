# pyiiif [![v0.1.0](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/uchicago-library/pyiiif/releases)

[![Build Status](https://travis-ci.org/uchicago-library/pyiiif.svg?branch=master)](https://travis-ci.org/uchicago-library/pyiiif) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/pyiiif/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/pyiiif?branch=master) [![Documentation Status](https://readthedocs.org/projects/uchicagolibrary-pyiiif/badge/?version=latest)](http://uchicagolibrary-pyiiif.readthedocs.io/en/latest/?badge=latest)

## Introduction

pyiiif is a library for working with the IIIF Presentation API 

It provides a pythonic interface to generating IIIF Presentation API records. The purpose is to reduce the amount of typing required and reduce amount of errors in creating large numbers of IIIF records. 

You can create a IIIF record by simply typing the following:

```python
from pyiiif.pres_api.twodotone.records import Manifest
r = Manifest("https://example.org/manifest")
r.type = "sc:Manifest"
r.label = "Fun with IIIF"
r.description = "This is my first IIIF manifest. Please be polite with your criticism"
str(r)
```

You have a properly formatted IIIF Manifest record with the correct @context, @type and @id attributes as well as a label and a description. The sequence list will be empty for now. From here, you just need to write the string into  a dictionary

And, for a more complicated example...

```python
import urllib.parse
from pyiiif.pres_api.twodotone.records import Manifest, Canvas, ImageResource, Annotation, Sequence

# start with a manifest object and remmeber like with every object 
# you create the uri has to be resolvable
# but, 404s are still acceptable
manifest = Manifest("http://example.org/foo")
manifest.type = "sc:Manifest"
manifest.label = "Fun with IIIF"
manifest.description = "This is my first IIIF manifest. Please be polite with your criticism"

# every good IIIF manifest has to have at least one sequence
sequence = Sequence("http://example.org/sequence/1")

# and now to make a simple canvas
canvas_id = "http://example.org/canvas/1"
canvas = Canvas(canvas_id)
canvas.label = "A Canvas"

# now to make an annotation for that canvas
annotate = Annotation("http://example.org/annotation/1", canvas_id)

# now to make an image resource to put in the canvas
img = ImageResource(
  "http",
  "example.org",
  "",
  urllib.parse.quote("/an_image.jpg", safe=""),
  "image/jpeg"
)

#  last but not least you have to put all the pieces together...
annotate.resource = img
canvas.images = [annotate]
sequence.canvases = [canvas]
manifest.sequences = [sequence]

# and voila! you have a IIIF manifest record!
str(manifest)
```

If all you care about is getting a nicely structured IIIF image api url without having to remember where to put all those forward slashes and how to percent-encoded characters in the identifier string, then you use the ImageApiUrl object

```python
from pyiiif.image_api.twodotone import ImageApiUrl
i = ImageApiUrl("https", "iiiif-server.lib.uchicago.edu", "", "default-photo.original.jpg")
i.to_image_url()
'https://iiif-server.lib.uchicago.edu/default-photo.original.jpg/full/full/0/default.jpg'
i.to_info_url()
'https://iiif-server.lib.uchicago.edu/default-photo.original.jpg/info.json'
```

## Quickstart

```shell
$ git clone git@github.com:uchicago-library/pyiiif
$ cd pyiiif
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements_dev.txt
$ pip install -r requirements.txt
$ python setup.py develop
$ pytest tests/
```

This will:

1. clone the repo onto your Linux/Unix system (in Windows I recommend using WSL and Ubuntu)
1. create a virtual environment in the repo working directory
1. activate the virtual environment
1. install the requirements for development (this includes pytest and all librarys for evaluating formatting, code coverage, et cetera)
1. install the third party libraries required for running the code
1. install the library into your virtual environment in development so that you won't have to run install every time you make changes to your code that you want to test
1. run the tests that are written for the project

# Footnotes
- [Complete documentation](https://uchicagolibrary-pyiiif.readthedocs.io)
- [IIIF or International Interoperable Image Framework](http://iiif.io/)
- [IIIF Presentation APIs](http://iiif.io/api/presentation/2.1/)

# Authors
- verbalhanglider <tdanstrom@uchicago.edu>
- Brian Balsamo <brian@brianbalsamo.com>
