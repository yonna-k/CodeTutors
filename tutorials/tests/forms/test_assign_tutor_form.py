from django import forms
from django.test import TestCase
from tutorials.forms.lesson_forms import AssignTutorForm
from tutorials.models.tutor_model import Tutor
from django.contrib.auth.hashers import make_password

class AssignTutorFormTest(TestCase):
    def setUp(self):
        #create sample tutors for testing
        self.tutor_1 = Tutor.objects.create(
            username="@testtutor",
            password=make_password('Password123'),
            first_name="Test",
            last_name="Tutor",
            email="testtutor@example.com",
            specializes_in_python=True,
            specializes_in_C=True,
            available_monday=True,
            available_tuesday=True,
            rate=9.00,  # Hourly rate in the preferred currency
        )

        self.tutor_2 = Tutor.objects.create(
            username="@testtutor2",
            password=make_password('Password123'),
            first_name="Test2",
            last_name="Tutor2",
            email="testtutor2@example.com",
            specializes_in_python=True,
            available_monday=True,
            available_wednesday=True,
            rate=10.00,  # Hourly rate in the preferred currency
        )



    def test_form_initializes_with_tutors(self):
        #test that the form initializes with the provided queryset of tutors
        form = AssignTutorForm(tutors=Tutor.objects.all())
        self.assertEqual(list(form.fields['tutor'].queryset), [self.tutor_1, self.tutor_2])

    def test_form_initializes_with_empty_queryset(self):
        #test that the form initializes with an empty queryset if no tutors are provided
        form = AssignTutorForm()
        self.assertEqual(list(form.fields['tutor'].queryset), [])

    def test_label_from_instance(self):
        #test that tutor names are formatted correctly
        form = AssignTutorForm(tutors=Tutor.objects.all())
        labels = [form.fields['tutor'].label_from_instance(t) for t in Tutor.objects.all()]
        self.assertEqual(labels, ["Test Tutor", "Test2 Tutor2"])

    def test_form_is_valid_with_valid_tutor(self):
        #test that the form is valid when a valid tutor is selected
        form = AssignTutorForm(data={'tutor': self.tutor_1.id}, tutors=Tutor.objects.all())
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_tutor(self):
        #test that the form raises an error if no tutor is selected
        form = AssignTutorForm(data={'tutor': None}, tutors=Tutor.objects.all())
        self.assertFalse(form.is_valid())
        self.assertIn("Please select a tutor.", form.errors['__all__'])

    def test_form_is_invalid_with_nonexistent_tutor(self):
        #test that the form raises an error if a nonexistent tutor is selected
        form = AssignTutorForm(data={'tutor': 999}, tutors=Tutor.objects.all())
        self.assertFalse(form.is_valid())
        self.assertIn("Select a valid choice. That choice is not one of the available choices.", form.errors['tutor'])
    
    def test_form_handles_dynamic_queryset(self):
        #test that the form respects the dynamically provided queryset
        form = AssignTutorForm(tutors=Tutor.objects.filter(first_name="Test"))
        self.assertEqual(list(form.fields['tutor'].queryset), [self.tutor_1])
