from django.test import TestCase
from django.urls import reverse
from .models import Review, Place
from .forms import PlaceForm
import json

class YourAppTest(TestCase):
    def setUp(self):
        self.Place = Place.objects.create(
            long=12.345678,
            lat=45.678901,
            name="Test Place",
            average_rating=4.5,
            place_description="Test description",
            name_slug="test-place"
        )



class YourAppTest(TestCase):
    def test_response_status_code_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
    
    def test_response_status_code_map(self):
        response = self.client.get(reverse('map'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "map.html")

    def test_response_status_code_add(self):
        response = self.client.get(reverse("add"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "add.html")

    def test_response_status_code_logout(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)

    def test_place_form_valid(self):
        form = PlaceForm(data={
                "long": 60,
                "lat": -60,
                "name": "test",
                "place_description": "test",
            } 
        )
        self.assertTrue(form.is_valid())

    def test_place_form_invalid(self):
        form = PlaceForm(data={})
        self.assertFalse(form.is_valid())

        self.assertEqual(len(form.errors),5)
        
    

