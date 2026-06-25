from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cravely_app.models import Recipe, Tag, Ingredient, RecipeIngredient


class HomepageViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.recipe = Recipe.objects.create(
            title='Test Recipe',
            description='A test recipe',
            cooking_time=10,
            portions=2,
            steps='Step 1|Step 2',
            author=self.user,
        )

    def test_homepage_returns_200(self) -> None:
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

    def test_homepage_contains_recipe(self) -> None:
        response = self.client.get(reverse('homepage'))
        self.assertContains(response, 'Test Recipe')


class RecipepageViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.recipe = Recipe.objects.create(
            title='Spaghetti',
            description='Italian classic',
            cooking_time=30,
            portions=4,
            steps='Boil water|Cook pasta|Add sauce',
            author=self.user,
        )

    def test_recipepage_returns_200(self) -> None:
        response = self.client.get(reverse('recipepage', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)

    def test_recipepage_contains_title(self) -> None:
        response = self.client.get(reverse('recipepage', args=[self.recipe.id]))
        self.assertContains(response, 'Spaghetti')

    def test_recipepage_returns_404_for_missing_recipe(self) -> None:
        response = self.client.get(reverse('recipepage', args=[99999]))
        self.assertEqual(response.status_code, 404)


class AddRecipeViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_add_recipe_requires_login(self) -> None:
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response['Location'])

    def test_add_recipe_get_returns_200_when_logged_in(self) -> None:
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('add_recipe'))
        self.assertEqual(response.status_code, 200)

    def test_add_recipe_creates_recipe(self) -> None:
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(reverse('add_recipe'), {
            'title': 'New Recipe',
            'description': 'A new recipe',
            'cooking_time': 15,
            'portions': 2,
            'steps': 'Step one',
        })
        self.assertEqual(Recipe.objects.filter(title='New Recipe').count(), 1)

    def test_add_recipe_sets_author(self) -> None:
        self.client.login(username='testuser', password='pass123')
        self.client.post(reverse('add_recipe'), {
            'title': 'My Recipe',
            'description': 'Description',
            'cooking_time': 10,
            'portions': 1,
            'steps': 'Only step',
        })
        recipe = Recipe.objects.get(title='My Recipe')
        self.assertEqual(recipe.author, self.user)


class ToggleSaveViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.recipe = Recipe.objects.create(
            title='Favourite Recipe',
            description='Delicious',
            cooking_time=20,
            portions=2,
            steps='Cook it',
            author=self.user,
        )

    def test_toggle_save_requires_login(self) -> None:
        response = self.client.post(reverse('toggle_save', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 302)

    def test_toggle_save_saves_recipe(self) -> None:
        self.client.login(username='testuser', password='pass123')
        self.client.post(reverse('toggle_save', args=[self.recipe.id]))
        self.assertIn(self.recipe, self.user.favorite_recipes.all())

    def test_toggle_save_unsaves_recipe(self) -> None:
        self.client.login(username='testuser', password='pass123')
        self.client.post(reverse('toggle_save', args=[self.recipe.id]))
        self.client.post(reverse('toggle_save', args=[self.recipe.id]))
        self.assertNotIn(self.recipe, self.user.favorite_recipes.all())


class LookupViewTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.tag = Tag.objects.create(name='vegan')
        self.recipe1 = Recipe.objects.create(
            title='Vegan Salad',
            description='Healthy salad',
            cooking_time=10,
            portions=2,
            steps='Mix everything',
            author=self.user,
        )
        self.recipe1.tags.add(self.tag)
        self.recipe2 = Recipe.objects.create(
            title='Beef Stew',
            description='Hearty stew',
            cooking_time=90,
            portions=4,
            steps='Brown meat|Add vegetables|Simmer',
            author=self.user,
        )

    def test_lookup_returns_200(self) -> None:
        response = self.client.get(reverse('lookup'))
        self.assertEqual(response.status_code, 200)

    def test_lookup_by_title(self) -> None:
        response = self.client.get(reverse('lookup'), {'q': 'Vegan'})
        self.assertContains(response, 'Vegan Salad')
        self.assertNotContains(response, 'Beef Stew')

    def test_lookup_by_tag(self) -> None:
        response = self.client.get(reverse('lookup'), {'filter': 'vegan'})
        self.assertContains(response, 'Vegan Salad')
        self.assertNotContains(response, 'Beef Stew')

    def test_lookup_no_query_returns_all(self) -> None:
        response = self.client.get(reverse('lookup'))
        self.assertContains(response, 'Vegan Salad')
        self.assertContains(response, 'Beef Stew')
