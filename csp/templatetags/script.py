from django import template
from django.template.base import TextNode


def do_dynamic_script(parser, token):
    nodelist = parser.parse(('enddynamicscript',))
    parser.delete_first_token()
    return ScriptNode(True, nodelist)

def do_script(parser, token):
    nodelist = parser.parse(('endscript',))
    parser.delete_first_token()
    return ScriptNode(False, nodelist)


class ScriptNode(template.Node):
    def __init__(self, dangerous, nodelist):
        self.dangerous = dangerous
        self.nodelist = nodelist

    def render(self, context):
        comment = ''
        if not self.dangerous:
            if len(self.nodelist) > 1 or len(self.nodelist) > 0\
                    and type(self.nodelist[0]) != TextNode:
                        return '<!-- script clobbered by django-csp -->'
        return comment\
            + "<script nonce=\"%s\">" % (unicode(context['csp_nonce']))\
            + self.nodelist.render(context) + '</script>'

register = template.Library()
register.tag('script', do_script)
register.tag('dynamicscript', do_dynamic_script)
