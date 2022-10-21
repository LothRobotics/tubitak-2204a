from django import template
register = template.Library()

@register.simple_tag
def format_school_name(school_name: str):
    return school_name.split('-')[1].strip()