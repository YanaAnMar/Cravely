import django
import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from cravely_app.models import Recipe, Ingredient, Tag, RecipeIngredient, Profile


class TagModelTest(TestCase):
    def setUp(self) -> None:
        self.tag = Tag.objects.create(name='quick_meals')

    def test_str_returns_name(self) -> None:
        self.assertEqual(str(self.tag), 'quick_meals')

    def test_display_name_formats_correctly(self) -> None:
        self.assertEqual(self.tag.display_name, 'Quick Meals')

    def test_display_name_single_word(self) -> None:
        tag = Tag.objects.create(name='vegan')
        self.assertEqual(tag.display_name, 'Vegan')


class IngredientModelTest(TestCase):
    def setUp(self) -> None:
        self.ingredient = Ingredient.objects.create(name='salt')

    def test_str_returns_name(self) -> None:
        self.assertEqual(str(self.ingredient), 'salt')

    def test_ingredient_name_is_unique(self) -> None:
        with self.assertRaises(Exception):
            Ingredient.objects.create(name='salt')


class RecipeModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.recipe = Recipe.objects.create(
            title='Pasta Carbonara',
            description='Classic Italian pasta dish',
            cooking_time=20,
            portions=2,
            steps='Boil pasta|Fry bacon|Mix eggs and cheese|Combine',
            author=self.user,
        )

    def test_str_returns_title(self) -> None:
        self.assertEqual(str(self.recipe), 'Pasta Carbonara')

    def test_recipe_has_author(self) -> None:
        self.assertEqual(self.recipe.author, self.user)

    def test_recipe_default_likes(self) -> None:
        self.assertEqual(self.recipe.likes, 0)

    def test_recipe_in_author_created_recipes(self) -> None:
        self.assertIn(self.recipe, self.user.created_recipes.all())


class RecipeIngredientModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.recipe = Recipe.objects.create(
            title='Omelette',
            description='Simple omelette',
            cooking_time=5,
            portions=1,
            steps='Beat eggs|Cook in pan',
            author=self.user,
        )
        self.ingredient = Ingredient.objects.create(name='eggs')
        self.recipe_ingredient = RecipeIngredient.objects.create(
            recipe=self.recipe,
            ingredient=self.ingredient,
            quantity='2 pieces',
        )

    def test_str_returns_formatted_string(self) -> None:
        expected = '2 pieces of eggs in Omelette'
        self.assertEqual(str(self.recipe_ingredient), expected)


class ProfileModelTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_profile_auto_created_on_user_creation(self) -> None:
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)

    def test_str_returns_username(self) -> None:
        self.assertEqual(str(self.user.profile), 'testuser')

    def test_profile_blacklist_starts_empty(self) -> None:
        self.assertEqual(self.user.profile.blacklist.count(), 0)

    def test_blacklist_add_ingredient(self) -> None:
        ingredient = Ingredient.objects.create(name='peanuts')
        self.user.profile.blacklist.add(ingredient)
        self.assertIn(ingredient, self.user.profile.blacklist.all())
