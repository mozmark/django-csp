from django import template
import django
import datetime

def do_script(parser, token):
    tag_name = None
    arg = None
    try:
        tag_name, arg = token.split_contents()
    except ValueError:
        tag_name = token.contents
    if arg:
        if not (arg[0] == arg[-1] and arg[0] in ('"', "'")):
            raise template.TemplateSyntaxError("%r tag's argument should be in quotes" % tag_name)
    else:
        arg = ''

    nodelist = parser.parse(('endscript',))
    parser.delete_first_token()

    return ScriptNode(arg[1:-1], nodelist)

class ScriptNode(template.Node):
    def __init__(self, arg, nodelist):
        self.dangerous = 'dangerous' == arg
        self.nodelist = nodelist

    def render(self, context):
        comment = ''
        if not self.dangerous:
            if len(self.nodelist) > 1\
            or len(self.nodelist) > 0\
            and type(self.nodelist[0]) != django.template.base.TextNode:
                return '<!-- dangerous script clobbered by django-csp -->'
        return comment+"<script nonce=\"%s\">"%(unicode(context['csp_nonce']))+self.nodelist.render(context)+'</script>'

register = template.Library()
register.tag('script',do_script)
