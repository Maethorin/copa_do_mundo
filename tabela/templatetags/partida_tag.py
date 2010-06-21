# -*- coding: utf-8 -*-

from django.template import Library, Node, NodeList, Template, TemplateSyntaxError
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string

register = Library()

class PartidaTag(Node):        
    def render(self, context):
        return render_to_string('partida_tag.html', context)    

@register.tag
def partida_tag(parser, token):
    return PartidaTag()
