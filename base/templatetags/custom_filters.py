from django import template

register = template.Library()

@register.filter
def shorten_number(number):
    suffixes = ['', 'K', 'M', 'B']
    suffix_index = 0
    while number >= 1000 and suffix_index < len(suffixes) - 1:
        suffix_index += 1
        number /= 1000

    if suffixes[suffix_index] == '':
        result = f"{number:.0f}"
    else :
        result = f"{number:.1f}"

    result += suffixes[suffix_index]

    return result

