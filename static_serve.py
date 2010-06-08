#!/usr/bin/env python
# encoding: utf-8

from django.views.static import serve
from django.http import Http404
from copa_do_mundo.locator import locate_resource_dirs
from django.conf import settings

def serve_media(request, path):
    directories = [settings.MEDIA_ROOT]
    directories.extend(locate_resource_dirs("media"))

    response = None
    for root in directories:
        try:
            response = serve(request, path, root)
            break
        except Http404, e:
            continue

    if not response:
        msg = u'O arquivo "%s" não pôde ser encontrado em nenhum dos ' \
              'caminhos a seguir: "%s"'
        lookup_paths = '%s' % '", "'.join(directories)

        raise Http404(msg % (path, lookup_paths))

    return response
