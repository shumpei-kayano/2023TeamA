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
#数値に対してのみ使用可能。文字列の場合、エラーが出る
@register.filter
def to_currency(value):
    try:
        # value = float(value)
        return "{:,}".format(value)
    except ValueError:
        return value

@register.filter
def meter_value(value, arg):
    #valueをargで割る
    return round(value / float(arg))