from django import template

register = template.Library()

@register.filter
def str_replace(value, arg):
    """
    Replaces occurrences of 'old' with 'new' in a string.
    Usage: {{ value|str_replace:"old_string,new_string" }}
    """
    try:
        old_string, new_string = arg.split(',')
        return value.replace(old_string, new_string)
    except ValueError:
        return value