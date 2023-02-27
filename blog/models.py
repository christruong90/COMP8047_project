from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title + " | " + str(self.author)

class Developer(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Condo(models.Model):
    title = models.CharField(max_length=100)
    condo_image = models.ImageField(null=True, blank=True, upload_to="images/")
    pet_friendly = models.BooleanField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    architect = models.CharField(max_length=255)
    number_of_units = models.IntegerField()
    floors = models.IntegerField()
    built_in = models.IntegerField(
        validators=[
            MaxValueValidator(2100),
            MinValueValidator(1900)
        ]
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class ReviewRating(models.Model):
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_service = models.FloatField()
    build_quality = models.FloatField()
    amenities = models.FloatField()
    location = models.FloatField()
    review_title = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    would_reviewer_recommend = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.review_title