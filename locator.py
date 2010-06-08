#!/usr/bin/env python
# encoding: utf-8

from os import walk
from os.path import abspath, join, exists
from glob import glob
import fnmatch

from django.conf import settings

def locate_files(root, pattern, recursive):
    if recursive:
        return_files = []
        for path, dirs, files in walk(root):
            for filename in fnmatch.filter(files, pattern):
                return_files.append(join(path, filename))
        return return_files
    else:
        return glob(join(root, pattern))

def locate_resource_dirs(complement, pattern="*.*", recursive=True):
    dirs = []
    for app in settings.INSTALLED_APPS:
        fromlist = ""

        if len(app.split("."))>1:
            fromlist = ".".join(app.split(".")[1:])

        module = __import__(app, fromlist=fromlist)
        app_dir = abspath("/" + "/".join(module.__file__.split("/")[1:-1]))

        resource_dir = join(app_dir, complement)

        if exists(resource_dir) and locate_files(resource_dir, pattern, recursive):
            dirs.append(resource_dir)

    return dirs
