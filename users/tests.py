from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Profile
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io
import os


class ProfileModelTest(TestCase):
    """Test the Profile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_creation(self):
        """Test that a profile is created automatically when a user is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, Profile)
    
    def test_profile_str_method(self):
        """Test the string representation of a profile"""
        self.assertEqual(str(self.user.profile), 'testuser Profile')
    
    def test_profile_default_image(self):
        """Test that the default image is set"""
        self.assertEqual(self.user.profile.image.name, 'default.jpg')


class UserRegisterFormTest(TestCase):
    """Test the UserRegisterForm"""
    
    def test_user_register_form_valid(self):
        """Test that the form is valid with correct data"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_user_register_form_invalid_password_mismatch(self):
        """Test that the form is invalid when passwords don't match"""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123!',
            'password2': 'differentpass123!'
        }
        form = UserRegisterForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_user_register_form_has_email_field(self):
        """Test that the email field is present"""
        form = UserRegisterForm()
        self.assertIn('email', form.fields)
    
    def test_user_register_form_fields_order(self):
        """Test that fields are in the correct order"""
        form = UserRegisterForm()
        self.assertEqual(
            list(form.fields.keys()),
            ['username', 'email', 'password1', 'password2']
        )


class UserUpdateFormTest(TestCase):
    """Test the UserUpdateForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_update_form_valid(self):
        """Test that the form is valid with correct data"""
        form_data = {
            'username': 'updateduser',
            'email': 'updated@example.com'
        }
        form = UserUpdateForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_user_update_form_has_email_field(self):
        """Test that the email field is present"""
        form = UserUpdateForm(instance=self.user)
        self.assertIn('email', form.fields)


class ProfileUpdateFormTest(TestCase):
    """Test the ProfileUpdateForm"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_update_form_has_image_field(self):
        """Test that the image field is present"""
        form = ProfileUpdateForm(instance=self.user.profile)
        self.assertIn('image', form.fields)


class RegisterViewTest(TestCase):
    """Test the register view"""
    
    def setUp(self):
        self.client = Client()
    
    def test_register_view_get(self):
        """Test that the register page loads correctly"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
        self.assertIsInstance(response.context['form'], UserRegisterForm)
    
    def test_register_view_post_valid(self):
        """Test that a user can be registered"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123!',
            'password2': 'testpass123!'
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().username, 'newuser')
        # Should redirect to login page
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
    
    def test_register_view_post_invalid(self):
        """Test that invalid data does not create a user"""
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpass123!',
            'password2': 'differentpass!'
        })
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    """Test the profile view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_profile_view_redirect_if_not_logged_in(self):
        """Test that non-logged in users are redirected to login"""
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/login/'))
    
    def test_profile_view_logged_in(self):
        """Test that logged in users can access the profile page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
    
    def test_profile_view_has_forms(self):
        """Test that the profile page has the update forms"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertIsInstance(response.context['u_form'], UserUpdateForm)
        self.assertIsInstance(response.context['p_form'], ProfileUpdateForm)
    
    def test_profile_view_update_user(self):
        """Test that the user can be updated"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('profile'), {
            'username': 'updateduser',
            'email': 'updated@example.com'
        })
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')


class LogoutViewTest(TestCase):
    """Test the logout view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_logout_view_redirects_to_login(self):
        """Test that logout redirects to login page"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))


class LoginViewTest(TestCase):
    """Test the login view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_login_view_get(self):
        """Test that the login page loads correctly"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
    
    def test_login_view_post_valid(self):
        """Test that a user can log in with valid credentials"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('blog-home'))
    
    def test_login_view_post_invalid(self):
        """Test that invalid credentials do not log in the user"""
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
