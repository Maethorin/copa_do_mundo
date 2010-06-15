#!/usr/bin/env python
# -*- coding: utf-8 -*-

import warnings
import sys
import nose

from os.path import dirname

from optparse import make_option
from django.core.management.base import BaseCommand

from copa_do_mundo import settings

class Command(BaseCommand):
    kind = 'unit'
    help = "Run unit tests"

    make_option("-C", "--capturar-log", action="store_true", dest="capturar_log", default=False),
    make_option("-f", "--file", dest="file", default=None),
    make_option("-a", "--app", dest="app", default=None),

    def handle(self, *args, **options):
        nose_argv = ['nosetests','-sd', '--verbosity=2']

        warnings.filterwarnings('ignore', '.*',)

        app = options.get('app', None)
        test_file = options.get('file', None)
        if app:
            apps = [app]
        else:
            apps = [a for a in settings.INSTALLED_APPS if not a.startswith('django') and a != 'south']

        capturar_log = options.get('capturar_log', False)
        if not capturar_log:
            nose_argv.append('--nologcapture')

        modules = []

        if not test_file:
            nose_argv.append('--with-coverage')
            nose_argv.append('--cover-inclusive')
            for app in apps:
                test_module_path = "%s.tests" % (app)

                try:
                    try:
                        module = getattr(__import__(test_module_path, locals(), globals(), [self.kind], 3), self.kind)
                    except AttributeError, e:
                        print u'Está faltando o módulo de testes %s.%s na sua django-app' % (test_module_path, self.kind)
                        raise SystemExit(1)

                    modules.append(module)

                except ImportError, e:
                    import traceback
                    sys.stderr.write(u'%s\n\n' % traceback.format_exc(e))
                    sys.stderr.write(u'Aparentemente a app "%s" não possui ' \
                                     'as subpastas "tests/%s" ou está ' \
                                     'faltando um arquivo __init__.py em ' \
                                     'cada uma delas\n' % (app, self.kind))

                    raise SystemExit(666)

                nose_argv.append("--cover-package=%s" % app)

            nose_argv.extend([dirname(x.__file__) for x in modules])

        else:
            nose_argv.append(test_file)

        ret = nose.run(argv=nose_argv)
        if ret:
            code = 0
        else:
            code = 1

        raise SystemExit(code)
