# pyiiif [![v0.0.1](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/uchicago-library/pyiiif/releases)

[![Build Status](https://travis-ci.org/uchicago-library/pyiiif.svg?branch=master)](https://travis-ci.org/uchicago-library/pyiiif) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/pyiiif/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/pyiiif?branch=master) [![Documentation Status](https://readthedocs.org/projects/uchicagolibrary-pyiiif/badge/?version=latest)](http://uchicagolibrary-pyiiif.readthedocs.io/en/latest/?badge=latest)

## Introduction

pyiiif is a library for working with  

It provides a pythonic interface to generating IIIF Presentation API records. The purpose is to reduce the amount of typing required and reduce amount of errors in creating large numbers of IIIF records. 

A person with a nominal amount of programming experience can create a IIIF record by simply typing the following:

```python
>>> from pyiiif.pres_api.twodotone.records import Manifest
>>> r = Manifest()
>>> r.id = "https://example.org/foo"
>>> r.type = "sc:Manifest"
>>> r.label = "Fun with IIIF"
>>> r.description = "This is my first IIIF manifest. Please be polite with your criticism"
>>> str(r)
```

And, you have a properly formatted IIIF Manifest record with the correct @context, @type and @id attributes as well as a a label and a description. The sequence list will be empty for now. From here, you just need to write the string into  a dicitonary

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
verbalhanglider <tdanstrom@uchicago.edu>
Brian Balsamo <brian@brianbalsamo.com>
