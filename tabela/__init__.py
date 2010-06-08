#!/usr/bin/env python
# encoding: utf-8

from os.path import dirname, abspath, join

VERSION = '0.0.1'
version = VERSION
__version__ = VERSION

def get_local_file(path):
    return (lambda *x: abspath(join(dirname(path), *x)))
