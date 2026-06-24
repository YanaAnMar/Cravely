from django.shortcuts import render, get_object_or_404
from .models import Recipe

# Create your views here.

def homepage(request):
    return render(request, '../templates/homepage.html')

def profile(request):
    return render(request, '../templates/profile.html')

def recipepage(request, recipe_id):
    single_recipe = get_object_or_404(Recipe, id=recipe_id)
    steps_list = single_recipe.steps.split('|')
    return render(request, 'recipepage.html', {
        'recipe': single_recipe,
        'steps_list': steps_list
    })

def saved_recipes(request):
    return render(request, '../templates/saved_recipes.html')

def add_recipe(request):
    return render(request, '../templates/add_recipe.html')

def lookup(request):
    query = request.GET.get('q', '')
    filters = request.GET.getlist('filter')
    fridge = request.GET.getlist('fridge')

    results = Recipe.objects.all()

    if query:
        results = results.filter(title__icontains=query)

    if filters:
        results = results.filter(tags__name__in=filters).distinct()

    if fridge:
        for ingredient_name in fridge:
            results = results.filter(ingredients__name__icontains=ingredient_name)

    return render(request, '../templates/lookup.html', {
        'results': results,
        'query': query,
        'active_filters': filters,
        'fridge': fridge,
    })