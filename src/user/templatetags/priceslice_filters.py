from django import template
import locale

register = template.Library()

# @register.filter
# def to_currency(value):
#     try:
#         locale.setlocale(locale.LC_ALL, 'ja_JP.UTF-8')
#     except locale.Error:
#         try:
#             locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
#         except locale.Error:
#             print('miss')
#             return value
#     conv = locale.currency(value, grouping=True, symbol=False)
#     return conv

@register.filter
def to_currency(value):
    return "{:,}".format(value)