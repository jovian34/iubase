from markdown import markdown as md

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def markitup(value):
    return md(value)
