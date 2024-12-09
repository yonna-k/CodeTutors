"""Tests for the tutor sign-up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from tutorials.forms.login_forms import TutorSignUpForm
from tutorials.models.user_models import User
from tutorials.models.tutor_model import Tutor
from tutorials.tests.helpers import LogInTester

class TutorSignUpViewTestCase(TestCase, LogInTester):
    """Tests of the tutor sign-up view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('tutor_sign_up')
        self.form_input = {
            'username': '@newtutor',
            'first_name': 'New',
            'last_name': 'Tutor',
            'email': 'newtutor@example.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'specialty': 'math',  # Example field for tutors, adjust as needed
        }

        self.user = User.objects.create_user(
            username="newtutor",
            password="tutorpassword123",
            first_name="New",
            last_name="Tutor",
            email="newtutor@example.com"
        )

        # Create the associated Tutor instance
        self.tutor = Tutor.objects.create(user=self.user)

    def test_tutor_sign_up_url(self):
        self.assertEqual(self.url, '/tutor_sign_up/')

    def test_get_tutor_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TutorSignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_tutor_sign_up(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, TutorSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_successful_tutor_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        response_url = reverse('tutor_dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'tutor_dashboard.html')
        user = User.objects.get(username=self.form_input['username'])
        self.assertEqual(user.first_name, self.form_input['first_name'])
        self.assertEqual(user.last_name, self.form_input['last_name'])
        self.assertEqual(user.email, self.form_input['email'])
        self.assertEqual(user.role, 'tutor')
        is_password_correct = check_password(self.form_input['new_password'], user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())


    def test_get_tutor_sign_up_redirects_when_logged_in(self):
        """Test that logged-in users are redirected to their appropriate dashboard."""
        # Log in the user
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)

        # Determine the expected template based on the user's role
        if self.user.role == 'student':
            expected_template = 'student_dashboard.html'
        elif self.user.role == 'tutor':
            expected_template = 'tutor_dashboard.html'
        elif self.user.role == 'admin':
            expected_template = 'admin_dashboard.html'
        else:
            self.fail(f"Unexpected role for user {self.user.username}: {self.user.role}")

        # Check redirection and template used
        redirect_url = reverse('dashboard')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, expected_template)
