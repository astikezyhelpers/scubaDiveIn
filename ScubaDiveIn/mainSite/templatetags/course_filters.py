from django import template

register = template.Library()

@register.filter(name='divide')
def divide(value, arg):
    try:
        if value is None:
            return 0
        return int(float(value)) / int(float(arg))
    except (ValueError, ZeroDivisionError, TypeError):
        return 0

@register.filter(name='multiply')
def multiply(value, arg):
    try:
        if value is None:
            return 0
        return int(float(value)) * int(float(arg))
    except (ValueError, TypeError):
        return 0 