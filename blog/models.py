from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

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

class Condo(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    body = models.TextField()
    condo_image = models.ImageField(null=True, blank=True, upload_to="images/")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')


class ReviewRating(models.Model):
    condo = models.ForeignKey(Condo, on_delete=models.CASCADE)
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
        return self.subject