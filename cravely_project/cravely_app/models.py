from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Ingredient(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    

class Recipe(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Summary of dish")
    cooking_time = models.IntegerField()
    portions = models.IntegerField(default=1)
    likes = models.IntegerField(default=0)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    tags = models.ManyToManyField(Tag, blank=True)
    steps = models.TextField(default="", help_text="Seperate steps with |")
    favorited_by = models.ManyToManyField(User, blank=True, related_name="favorite_recipes")

    def __str__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.recipe.title}"