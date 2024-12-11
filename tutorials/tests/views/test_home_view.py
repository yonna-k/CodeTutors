"""Tests of the home view."""
from django.test import TestCase
from django.urls import reverse
from tutorials.models.user_models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class HomeViewTestCase(TestCase):
    """Tests of the home view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('home')
        self.user = User.objects.get(username='@johndoe')


    def test_home_url(self):
        self.assertEqual(self.url,'/')

    def test_get_home(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')


    def test_get_home_redirects_when_logged_in(self):
        """Test that a logged-in user is redirected to the appropriate dashboard."""
        # Log in as @johndoe
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)

        # Determine the expected URL based on the role
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
            self.fail(f"Unexpected role for user @johndoe: {self.user.role}")

        # Check redirection and template used
        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, expected_template)
