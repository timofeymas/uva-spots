# https://django-crispy-forms.readthedocs.io/en/latest/

from django.forms import ModelForm, HiddenInput
from .models import UnacceptedPlace, Review
from django import forms

class PlaceForm(ModelForm):
    class Meta:
        model = UnacceptedPlace
        fields = ['name', 'place_description', 'long', 'lat']
        widgets = {
            'place_description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
            'long' : HiddenInput(),
            'lat' : HiddenInput(),
        }
        labels = {
            'name': 'Study Spot Name',
            'place_description': 'Place Description',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        long = cleaned_data.get('long')
        lat = cleaned_data.get('lat')

        if not long or not lat:
            raise forms.ValidationError("Please provide a marker on the above map for the location of your study spot.")

        return cleaned_data


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        ('--', '--'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    noise_level_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True, 
    )

    space_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    open_seats_rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True,
    )

    class Meta:
        model = Review
        fields = ['noise_level_rating', 'space_rating', 'open_seats_rating', 'rating_text']

class RejectionForm(ModelForm):
    class Meta:
        model = UnacceptedPlace
        fields = ['rejection_message']
        widgets = {
            'place_description': forms.Textarea(attrs={'rows': 5, 'cols': 40}),
        }
        labels = {
            'rejection_message': 'Reason For Rejection',
        }