# -*- coding: utf-8 -*-

from django.template import Library, Node, Template, TemplateSyntaxError

register = Library()

class TimeTag(Node):
    def __init__(self, lado):
        self.lado = lado
        
    def render(self, context):
        time = 'partida.time_1'
        if self.lado == 'direito':
            time = 'partida.time_2'
            
        time_template = '<div class="time %(lado)s {{%(time)s.abreviatura}}" title="{{%(time)s.nome}}">{%% if chaves %%}{{%(time)s.sigla|default:"NDF"}}{%% else %%}{{%(time)s.nome|default:"Não definido"}}{%% endif %%}</div>' % {'time': time, 'lado': self.lado}
        template = Template(time_template)
        
        return template.render(context)

@register.tag
def time_tag(parser, token):
    args = token.split_contents()

    if len(args) < 1:
        raise TemplateSyntaxError(
            u'E esperado pelo menos 1 argumento1: lado do time.'
        )

    lado = args[1]
    
    return TimeTag(lado)
