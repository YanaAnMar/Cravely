from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Recipe, RecipeIngredient, Ingredient, Tag
import json


# Create your views here.

def homepage(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.all()
    return render(request, '../templates/homepage.html', {'recipes': recipes})

def profile(request: HttpRequest, username: str) -> HttpResponse:
    user_profile = get_object_or_404(User, username=username)
    return render(request, 'profile.html', {
        'profile_user': user_profile
    })

def recipepage(request: HttpRequest, recipe_id: int) -> HttpResponse:
    single_recipe = get_object_or_404(Recipe, id=recipe_id)
    steps_list = single_recipe.steps.split('|')
    ingredients_list = RecipeIngredient.objects.filter(recipe=single_recipe)
    is_saved = request.user.is_authenticated and single_recipe.favorited_by.filter(id=request.user.id).exists()
    return render(request, 'recipepage.html', {
        'recipe': single_recipe,
        'steps_list': steps_list,
        'ingredients_list': ingredients_list,
        'is_saved': is_saved,
    })


@login_required
def toggle_save(request: HttpRequest, recipe_id: int) -> HttpResponse:
    if request.method == 'POST':
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if recipe.favorited_by.filter(id=request.user.id).exists():
            recipe.favorited_by.remove(request.user)
            saved = False
        else:
            recipe.favorited_by.add(request.user)
            saved = True
        return JsonResponse({'saved': saved})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def saved_recipes(request: HttpRequest) -> HttpResponse:
    saved = request.user.favorite_recipes.all()
    return render(request, '../templates/saved_recipes.html', {'saved': saved})

@login_required
def add_recipe(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        cooking_time = request.POST.get('cooking_time', 1)
        portions = request.POST.get('portions', 1)
        image = request.FILES.get('image')

        steps_str = '|'.join(s.strip() for s in request.POST.getlist('steps') if s.strip())

        recipe = Recipe.objects.create(
            title=title,
            description=description,
            cooking_time=int(cooking_time),
            portions=int(portions),
            steps=steps_str,
            author=request.user,
        )
        if image:
            recipe.image = image
            recipe.save()

        for tag_id in request.POST.getlist('tags'):
            try:
                recipe.tags.add(Tag.objects.get(id=tag_id))
            except Tag.DoesNotExist:
                pass

        ing_names = request.POST.getlist('ingredient_name')
        ing_qtys = request.POST.getlist('ingredient_quantity')
        for name, qty in zip(ing_names, ing_qtys):
            name, qty = name.strip(), qty.strip()
            if name and qty:
                ingredient = Ingredient.objects.filter(name__iexact=name).first()
                if not ingredient:
                    ingredient = Ingredient.objects.create(name=name)
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=qty)

        return redirect('recipepage', recipe_id=recipe.id)

    return render(request, '../templates/add_recipe.html', {'tags': Tag.objects.all()})


@login_required
def update_blacklist(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        is_json_request = request.content_type == 'application/json'

        if is_json_request:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
        else:
            data = request.POST

        action = data.get('action')
        ingredient_name = data.get('ingredient_name', '').strip()

        if action not in ['add', 'remove']:
            if is_json_request:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})
            return redirect('profile', username=request.user.username)

        if not ingredient_name:
            if is_json_request:
                return JsonResponse({'status': 'error', 'message': 'Ingredient name is required'})
            return redirect('profile', username=request.user.username)
        
        try:
            ingredient = Ingredient.objects.get(name__iexact=ingredient_name)
            profile = request.user.profile
            
            if action == 'add':
                profile.blacklist.add(ingredient)
            else:
                profile.blacklist.remove(ingredient)
                
            if is_json_request:
                return JsonResponse({'status': 'success'})
            return redirect('profile', username=request.user.username)
        except Ingredient.DoesNotExist:
            if is_json_request:
                return JsonResponse({'status': 'error', 'message': 'Ingredient not found'})
            return redirect('profile', username=request.user.username)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def lookup(request: HttpRequest) -> HttpResponse:
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
