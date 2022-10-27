import datetime

from django import template

GREETINGS = {
    12: 'Günaydın',
    18: 'İyi Günler',
    22: 'İyi akşamlar',
    4: 'İyi geceler'
}

register = template.Library()

@register.simple_tag
def get_greeting():
    local_datetime = datetime.datetime.now()
    local_hours = local_datetime.hour

    for greeting_hours, greeting_message in GREETINGS.items():
        if greeting_hours > local_hours:
            return greeting_message

    return "İyi günler"
    