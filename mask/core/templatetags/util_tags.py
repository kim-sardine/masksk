from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag
def current_domain():
    return 'http://192.168.99.100:8000' if settings.DEBUG else 'https://masksk.cc'
