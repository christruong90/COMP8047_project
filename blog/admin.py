from django.contrib import admin
from .models import Post, Condo, ReviewRating, Developer

# Register your models here.
# admin.site.register(Post)
admin.site.register(Condo)
admin.site.register(ReviewRating)
admin.site.register(Developer)