# pyiiif [![v0.0.1](https://img.shields.io/badge/version-0.0.1-blue.svg)](https://github.com/uchicago-library/pyiiif/releases)

[![Build Status](https://travis-ci.org/uchicago-library/pyiiif.svg?branch=master)](https://travis-ci.org/uchicago-library/pyiiif) [![Coverage Status](https://coveralls.io/repos/github/uchicago-library/pyiiif/badge.svg?branch=master)](https://coveralls.io/github/uchicago-library/pyiiif?branch=master) [![Documentation Status](https://readthedocs.org/projects/uchicagolibrary-pyiiif/badge/?version=latest)](http://uchicagolibrary-pyiiif.readthedocs.io/en/latest/?badge=latest)



Library code for working with the IIIF specifications


See the full documentation at https://pyiiif.readthedocs.io

## Introduction

pyiiif is a library for working with (at the moment) [IIIF Image APIs](http://iiif.io/api/image/2.1/) and [IIIF Presentation APIs](http://iiif.io/api/presentation/2.1/).

The goal of this library is to provide common utility functions for working with the APIs and records defined in these standards, as well as providing an object oriented interface for the creation of IIIF records.

For more information about IIIF technologies and specifications see [here](http://iiif.io/).

## Quickstart

```
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


# Authors
verbalhanglider <tdanstrom@uchicago.edu>
Brian Balsamo <brian@brianbalsamo.com>
