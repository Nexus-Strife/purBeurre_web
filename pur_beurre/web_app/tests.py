from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.


class IndexPageTestCase(TestCase):

    """Test the index"""

    def test_index_page(self):
        response = self.client.get(reverse('web_app:index'))
        self.assertEqual(response.status_code, 200)


class RegisterPageTestCase(TestCase):

    """Test the register page"""

    def test_register_page(self):
        response = self.client.get(reverse('web_app:register'))
        self.assertEqual(response.status_code, 200)


class LoginPageTestCase(TestCase):

    """Test the login page"""

    def test_login_page(self):
        response = self.client.get(reverse('web_app:login'))
        self.assertEqual(response.status_code, 200)


class TestAPI(TestCase):

    def test_api_json(self):
        response = self.client.get('https://fr.openfoodfacts.org/categories.json')
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):

    """Create a fake user and test the login function"""

    def fake_user(self):

        self.username = "Fake"
        self.password = "User"
        self.email = "test@test.test"
        self.first_name = "Fake"
        self.last_name = "User"

        # Save the fake user
        User.objects.create_user(self.username, self.email, self.password, self.first_name, self.last_name)

    def test_login_good_values(self):

        """Test login with the fake user"""

        self.username = "test"
        self.password = "test"

        response = self.client.post(reverse('web_app:login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

    def test_login_wrong_values(self):

        """Test login with wrongs value"""

        self.username = "Not_Fake"
        self.password = "Wrong_Pass"

        response = self.client.post(reverse('web_app:login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)

