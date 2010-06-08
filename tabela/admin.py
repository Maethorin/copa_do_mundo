#!/usr/bin/env python
# encoding: utf-8

"""
admin.py

Created by Marcio Amado Duarte Santana on 2010-05-29.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import sys
import os

from django.contrib import admin
from copa_do_mundo.tabela.models import *

admin.site.register(Grupo)
admin.site.register(Time)
admin.site.register(Partida)