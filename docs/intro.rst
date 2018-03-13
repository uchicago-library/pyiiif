Introduction
============

pyiiif is a library for working with  

It provides a pythonic interface to generating IIIF Presentation API records. The purpose is to reduce the amount of typing required and reduce amount of errors in creating large numbers of IIIF records. 

A person with a nominal amount of programming experience can create a IIIF record by simply typing the following:

.. code-block: python
    >>> from pyiiif.pres_api.twodotone.records import Manifest
    >>> r = Manifest(
    >>> r.id = "https://example.org/foo"
    >>> r.type = "sc:Manifest"
    >>> r.label = "Fun with IIIF"
    >>> r.description = "This is my first IIIF manifest. Please be polite with your criticism"
    >>> str(r)

And, you have a properly formatted IIIF Manifest record with the correct @context, @type and @id attributes as well as a a label and a description. The sequence list will be empty for now. From here, you just need to write the string into  a dicitonary

