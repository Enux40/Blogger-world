from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class UserTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_register_page_status_code(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'a_more_complex_password',
            'password2': 'a_more_complex_password',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_user_registration_password_mismatch(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password1': 'a_more_complex_password',
            'password2': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The two password fields didn’t match.")

    def test_login_page_status_code(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirects after successful login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profile_page_unauthenticated(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)  # Redirects to login page
        self.assertRedirects(response, '/login/?next=/profile/')

    def test_profile_page_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
