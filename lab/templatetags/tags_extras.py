from django import template

register = template.Library()

@register.filter
def get_at_index(list, index):
    return list[index]

@register.filter
def get_index_from_value(list, val):
    return list.index(val)