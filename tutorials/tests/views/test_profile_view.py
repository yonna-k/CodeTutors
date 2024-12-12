"""Tests for the profile view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tutorials.forms.login_forms import UserForm
from tutorials.models.user_models import User
from tutorials.tests.helpers import reverse_with_next

class ProfileViewTest(TestCase):
    """Test suite for the profile view."""

    fixtures = [
        'tutorials/tests/fixtures/default_user.json',
        'tutorials/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('profile')
        self.form_input = {
            'first_name': 'John2',
            'last_name': 'Doe2',
            'username': '@johndoe2',
            'email': 'johndoe2@example.org',
        }

    def test_profile_url(self):
        self.assertEqual(self.url, '/profile/')

    def test_get_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertEqual(form.instance, self.user)

    def test_get_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_profile_update(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_unsuccessful_profile_update_due_to_duplicate_username(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['username'] = '@janedoe'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, UserForm))
        self.assertTrue(form.is_bound)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, '@johndoe')
        self.assertEqual(self.user.first_name, 'John')
        self.assertEqual(self.user.last_name, 'Doe')
        self.assertEqual(self.user.email, 'johndoe@example.org')

    def test_successful_profile_update(self):
        """Test that a valid profile update saves changes and redirects to the appropriate dashboard."""
        self.client.login(username=self.user.username, password='Password123')
        before_count = User.objects.count()

        # Make a POST request to update the profile
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()

        # Assert that no new user has been created
        self.assertEqual(after_count, before_count)

        # Refresh the user instance from the database
        self.user.refresh_from_db()

        # Assert the user's attributes have been updated
        self.assertEqual(self.user.first_name, self.form_input['first_name'])
        self.assertEqual(self.user.last_name, self.form_input['last_name'])
        self.assertEqual(self.user.username, self.form_input['username'])
        self.assertEqual(self.user.email, self.form_input['email'])

        # Determine the expected redirect based on the user's role
        if self.user.role == 'student':
            expected_redirect_url = reverse('student_dashboard')
        elif self.user.role == 'tutor':
            expected_redirect_url = reverse('tutor_dashboard')
        elif self.user.role == 'admin':
            expected_redirect_url = reverse('admin_dashboard')
        else:
            self.fail(f"Unexpected role for user {self.user.username}: {self.user.role}")

        # Assert the user is redirected to the appropriate dashboard
        self.assertRedirects(response, expected_redirect_url)


    def test_post_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.post(self.url, self.form_input)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
