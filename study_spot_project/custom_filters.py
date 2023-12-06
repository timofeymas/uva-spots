# https://django-filter.readthedocs.io/en/stable/
from django import template

register = template.Library()

@register.filter
def star_rating(value):
    value = float(value)
    full_stars = int(value)
    remainder = value - full_stars
    empty_stars = int(5 - value)
    full_stars_str = u"\u2605" * full_stars
    half_star_str = u"\u2BEA" if remainder == 0.5 else ""
    empty_stars_str = u"\u2606" * empty_stars

    return full_stars_str + half_star_str + empty_stars_str
