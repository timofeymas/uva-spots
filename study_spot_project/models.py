from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

class Place(models.Model):
    long = models.DecimalField(max_digits=20, decimal_places=16)
    lat = models.DecimalField(max_digits=20, decimal_places=16)
    name = models.CharField(max_length=100)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    average_noise = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    average_space = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    average_open_seats = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    place_description = models.CharField(max_length=200)
    name_slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('map')
    
    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Place, self).save(*args, **kwargs)

    def find_average_rating(self):
        reviews = Review.objects.filter(place = self)
        if reviews:
            overall_sum = 0
            noise_sum = 0
            space_sum = 0
            open_seats_sum = 0
            for review in reviews:
                overall_sum += review.overall_rating
                noise_sum += review.noise_level_rating
                space_sum += review.space_rating
                open_seats_sum += review.open_seats_rating
            self.average_rating = round((overall_sum / len(reviews)), 2)
            self.average_noise = round((noise_sum / len(reviews)), 2)
            self.average_space = round((space_sum / len(reviews)), 2)
            self.average_open_seats = round((open_seats_sum / len(reviews)), 2)
            self.save()


class UnacceptedPlace(models.Model):
    long = models.DecimalField(max_digits=20, decimal_places=16)
    lat = models.DecimalField(max_digits=20, decimal_places=16)
    name = models.CharField(max_length=100, unique=True, error_messages={'unique':"A study spot with this name already exists (if you dont see it on the map it might not be approved yet)"})
    place_description = models.CharField(max_length=200)
    name_slug = models.SlugField(unique=True)
    rejection_message = models.CharField(max_length=200, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE, default="")

    def get_absolute_url(self):
        return reverse('map')

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(UnacceptedPlace, self).save(*args, **kwargs)


class Review(models.Model):
    overall_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # not inputed by the user, is calculated based on the other 3 ratings
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    noise_level_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    space_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    open_seats_rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    rating_text = models.CharField(max_length=400)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def calculate_overall_rating(self):
        overall = (self.noise_level_rating + self.space_rating + self.open_seats_rating) / 3
        self.overall_rating = round(overall, 2)

    def save(self, *args, **kwargs):
        self.calculate_overall_rating()
        super().save(args, kwargs)
        Place.find_average_rating(self.place)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_seen_modal = models.BooleanField(default=False)
    deletion_message = models.TextField(blank=True, null=True)