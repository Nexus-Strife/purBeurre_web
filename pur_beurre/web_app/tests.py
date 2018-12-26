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


class LoginTestCase(TestCase):

    """Create a fake user and test the login function"""

    def fakeUser(self):

        self.username = "test"
        self.password = "test"
        self.email = "test@test.test"
        self.first_name = "testeur"
        self.last_name = "foo"

        # Save the fake user
        User.objects.create_user(self.username, self.email, self.password)

    def test_login_good_values(self):

        """Test login with the fake user"""

        response = self.client.post(reverse('web_app:login'), {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 200)


