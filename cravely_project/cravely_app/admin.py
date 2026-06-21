from django.contrib import admin
from .models import Recipe, Ingredient, Tag, RecipeIngredient, Profile

class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1 

class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]

admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(RecipeIngredient)
admin.site.register(Profile)