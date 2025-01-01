import os
import uuid
from django import template

register = template.Library()


@register.simple_tag(name="cache_bust")
def cache_bust():
    version = os.environ.get("PROJECT_VERSION")
    if bool(int(os.environ.get("DEVELOP"))):
        version = uuid.uuid1()    
    return f"__v__={version}"
