from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """כפל שני ערכים"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """חלוקת שני ערכים"""
    try:
        return float(value) / float(arg)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

@register.filter
def add(value, arg):
    """חיבור שני ערכים"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0

