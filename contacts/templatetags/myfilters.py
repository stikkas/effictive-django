__author__ = 'basa'
# encoding: utf-8

from django import template

register = template.Library()

@register.filter
def addcss(value, arg):
    return value.as_widget(attrs={'class': arg})
