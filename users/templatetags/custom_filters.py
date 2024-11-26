# users/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter(name='replace_underscore')
def replace_underscore(value):
    return value.replace('_', ' ')
