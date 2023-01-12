from django import template

register = template.Library()


@register.filter()
def sep_to_dot(value):
    return str(value).replace(',', '.')
