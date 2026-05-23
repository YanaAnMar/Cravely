from django.db import models
from django.contrib.auth.models import User

class Ingredient(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    cooking_time = models.IntegerField()
    likes = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient)
    favorited_by = models.ManyToManyField(User, blank=True, related_name="favorite_recipes")

    def __str__(self):
        return self.title