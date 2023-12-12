from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag(name="this_year")
def this_year():
    current = timezone.now()
    return current.year
