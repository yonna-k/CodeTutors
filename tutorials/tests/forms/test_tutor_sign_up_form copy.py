from django import forms
from django.test import TestCase
from tutorials.forms import TutorSignUpForm
from tutorials.models.user_models import User
from tutorials.models.tutor_model import Tutor

class TutorSignUpFormTestCase(TestCase):
    """Unit tests for the tutor sign up form."""

    def setUp(self):
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': '@johnsmith',
            'email': 'johnsmith@example.org',
            'new_password': 'Password123',
            'password_confirmation': 'Password123',
            'specializes_in_python': 'Yes',
            'specializes_in_java': 'No',
            'rate' : '19.00'
        }

    def test_valid_tutor_sign_up_form(self):
        form = TutorSignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = TutorSignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        self.assertIn('specializes_in_python', form.fields)
        self.assertIn('specializes_in_java', form.fields)
        self.assertIn('new_password', form.fields)
        self.assertIn('password_confirmation', form.fields)
        self.assertIn('rate', form.fields)

    def test_specialization_fields_are_dropdowns(self):
        form = TutorSignUpForm()
        self.assertTrue(isinstance(form.fields['specializes_in_python'].widget, forms.Select))
        self.assertTrue(isinstance(form.fields['specializes_in_java'].widget, forms.Select))

    def test_new_password_and_password_confirmation_must_match(self):
        self.form_input['password_confirmation'] = 'WrongPassword123'
        form = TutorSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        form = TutorSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        form = TutorSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'PasswordABC'
        form = TutorSignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_saves_correctly(self):
        form = TutorSignUpForm(data=self.form_input)
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count + 1)
        user = User.objects.get(username='@johnsmith')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Smith')
        self.assertEqual(user.email, 'johnsmith@example.org')
        self.assertEqual(user.role, 'tutor')
        self.assertTrue(Tutor.objects.filter(user=user).exists())
