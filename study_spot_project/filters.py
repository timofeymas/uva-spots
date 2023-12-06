import django_filters
from django import forms
from django_filters import NumberFilter
# https://django-filter.readthedocs.io/en/stable/

RATING_CHOICES = [("", "")] + [(i, str(i)) for i in range(1, 6)]

#consulted Youtube Tutorial on implementing django-filters by The Dumbfounds: https://www.youtube.com/watch?v=nle3u6Ww6Xk
class PlaceFilter(django_filters.FilterSet):
    average_rating__gte = django_filters.NumberFilter(
        field_name='average_rating',
        lookup_expr='gte',
        widget=forms.Select(choices=RATING_CHOICES, attrs={'style': 'width: 3em; margin-left: 47px;'}),
    )
    average_noise__gte = django_filters.NumberFilter(
        field_name='average_noise',
        lookup_expr='gte',
        widget=forms.Select(choices=RATING_CHOICES, attrs={'style': 'width: 3em; margin-left: 50px;'}),
    )
    average_space__gte = django_filters.NumberFilter(
        field_name='average_space',
        lookup_expr='gte',
        widget=forms.Select(choices=RATING_CHOICES, attrs={'style': 'width: 3em; margin-left: 47px;'}),
    )
    average_open_seats__gte = django_filters.NumberFilter(
        field_name='average_open_seats',
        lookup_expr='gte',
        widget=forms.Select(choices=RATING_CHOICES, attrs={'style': 'width: 3em; margin-left: 11px;'}),
    )
