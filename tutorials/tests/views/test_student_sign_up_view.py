"""Tests for the student sign-up view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from tutorials.forms.login_forms import StudentSignUpForm
from tutorials.models.user_models import User
from tutorials.models.student_model import Student
from tutorials.tests.helpers import LogInTester

class StudentSignUpViewTestCase(TestCase, LogInTester):
    """Tests of the student sign-up view."""

    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('student_sign_up')
        self.form_input = {
            'username': '@newstudent',
            'first_name': 'New',
            'last_name': 'Student',
            'email': 'newstudent@example.com',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'level': 'BEGINNER',  # Example field for students, adjust as needed
        }

        # Create an existing student for other tests
        self.user = User.objects.create_user(
            username='teststudent',
            password='Password123',
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
            role='student',
        )
        self.student = Student.objects.create(user=self.user)

    def test_student_sign_up_url(self):
        self.assertEqual(self.url, '/sign_up/student/')

    def test_get_student_sign_up(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentSignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_student_sign_up(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, StudentSignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())

    def test_get_student_sign_up_redirects_when_logged_in(self):
        """Test that logged-in users are redirected to their appropriate dashboard."""
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url, follow=True)

        # Determine expected URL and template based on role
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

        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, expected_template)



    def test_successful_student_sign_up(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()

        self.assertEqual(after_count, before_count + 1)

        # Expect specific role-based URL and template
        expected_url = reverse('student_dashboard')
        expected_template = 'student_dashboard.html'

        self.assertRedirects(response, expected_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, expected_template)

        # Verify the created user data
        user = User.objects.get(username=self.form_input['username'])
        self.assertEqual(user.first_name, self.form_input['first_name'])
        self.assertEqual(user.last_name, self.form_input['last_name'])
        self.assertEqual(user.email, self.form_input['email'])
        self.assertEqual(user.role, 'student')
        is_password_correct = check_password(self.form_input['new_password'], user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
