from django import template
from .bad_words import words

register = template.Library()

@register.filter()
def censor(value):
    for word in reversed(words):
        value = value.replace(word, len(word)*'*')
    return f'{value}'