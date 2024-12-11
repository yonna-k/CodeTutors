"""Tests for the password view."""
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from tutorials.forms.login_forms import PasswordForm
from tutorials.models.user_models import User
from tutorials.tests.helpers import reverse_with_next

class PasswordViewTest(TestCase):
    """Test suite for the password view."""

    fixtures = [
        'tutorials/tests/fixtures/default_user.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('password')
        self.form_input = {
            'password': 'Password123',
            'new_password': 'NewPassword123',
            'password_confirmation': 'NewPassword123',
        }

    def test_password_url(self):
        self.assertEqual(self.url, '/password/')

    def test_get_password(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))

    def test_get_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_succesful_password_change(self):
        """Test successful password change redirects to the appropriate dashboard."""
        # Log in the user
        self.client.login(username=self.user.username, password='Password123')

        # Submit the password change form
        response = self.client.post(self.url, self.form_input, follow=True)

        # Determine the expected URL and template based on the user's role
        if self.user.role == 'student':
            expected_url = reverse('student_dashboard')
            expected_template = 'student_dashboard.html'
        elif self.user.role == 'tutor':
            expected_url = reverse('tutor_dashboard')
            expected_template = 'tutor_dashboard.html'
        elif self.user.role == 'admin':
            expected_url = reverse('admin_dashboard')
            expected_template = 'admin_dashboard.html'
        else:
            self.fail(f"Unexpected role for user {self.user.username}: {self.user.role}")

        # Verify the redirection and template used
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, expected_template)

        # Refresh the user instance to verify the password change
        self.user.refresh_from_db()
        is_password_correct = check_password('NewPassword123', self.user.password)
        self.assertTrue(is_password_correct)


    def test_password_change_unsuccesful_without_correct_old_password(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_password_change_unsuccesful_without_password_confirmation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['password_confirmation'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordForm))
        self.user.refresh_from_db()
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)

    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        is_password_correct = check_password('Password123', self.user.password)
        self.assertTrue(is_password_correct)
