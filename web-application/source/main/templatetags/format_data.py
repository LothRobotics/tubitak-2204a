from django import template

register = template.Library()

@register.simple_tag
def format_school_name(school_name: str):
    return school_name.split('-')[1].strip()

@register.simple_tag
def format_hashed_password(hashed_password: str):
    return hashed_password[:20] if len(hashed_password) >= 1 else "Tanımlanmamış Şifre"