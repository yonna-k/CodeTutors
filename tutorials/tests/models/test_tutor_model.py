from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from tutorials.models.tutor_model import Tutor  

class TutorModelTestCase(TestCase):
    """Unit tests for the Tutor model."""

    def setUp(self):
        # Create a tutor instance for testing
        self.tutor = Tutor.objects.create(
            username='@testtutor',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Tutor',
            email='testtutor@example.com',
            rate=25.00,  # Hourly rate
            specializes_in_python=True,  # Setting some specialties
            available_monday=True  # Available on Monday
        )

    def test_valid_tutor(self):
        """Test that a valid tutor instance passes validation."""
        self._assert_tutor_is_valid()

    def test_specialties_method(self):
        """Test the get_specialties method."""
        self.assertEqual(self.tutor.get_specialties(), ['Python'])

    def test_availability_method(self):
        """Test the get_availability method."""
        self.assertEqual(self.tutor.get_availability(), ['Monday'])

    def test_default_specialties(self):
        """Test default values for specialties (should be False)."""
        tutor_without_specialties = Tutor.objects.create(
            username='@newtutor',
            password=make_password('Password123'),
            first_name='New',
            last_name='Tutor',
            email='newtutor@example.com',
            rate=30.00,
        )
        self.assertEqual(tutor_without_specialties.get_specialties(), [])

    def test_default_availability(self):
        """Test default values for availability (should be False)."""
        tutor_without_availability = Tutor.objects.create(
            username='@tutorwithoutavailability',
            password=make_password('Password123'),
            first_name='No',
            last_name='Availability',
            email='noavailability@example.com',
            rate=30.00,
        )
        self.assertEqual(tutor_without_availability.get_availability(), [])

    def test_rate_validation(self):
        """Test rate field validation (should not be negative)."""
        tutor_with_invalid_rate = Tutor(
            username='@invalidrate',
            password=make_password('Password123'),
            first_name='Invalid',
            last_name='Rate',
            email='invalidrate@example.com',
            rate=-10.00,
        )
        with self.assertRaises(ValidationError):
            tutor_with_invalid_rate.full_clean()  # This should raise a validation error

    def test_str_method(self):
        """Test the __str__ method."""
        self.assertEqual(str(self.tutor), 'Test - Python (Available)')  # Adjust if you want 'None' or the actual specialty

    # Helpers
    def _assert_tutor_is_valid(self):
        """Helper method to assert tutor instance is valid."""
        try:
            self.tutor.full_clean()
        except ValidationError:
            self.fail('Test tutor should be valid')

    def _assert_tutor_is_invalid(self):
        """Helper method to assert tutor instance is invalid."""
        with self.assertRaises(ValidationError):
            self.tutor.full_clean()
