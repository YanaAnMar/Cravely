from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        return self.name.replace('_', ' ').title()
    

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
    image = models.ImageField(upload_to='recipe_photos/', blank=True, null=True)

    def __str__(self):
        return self.title
    
class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.quantity} of {self.ingredient.name} in {self.recipe.title}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='profile_photos/', default='profile_photos/default_pfp.png', blank=True)
    blacklist = models.ManyToManyField(Ingredient, blank=True, related_name='blacklisted_by')

    def __str__(self):
        return self.user.username
    


from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()