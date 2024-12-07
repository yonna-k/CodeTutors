from django.core.exceptions import ValidationError
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from tutorials.models import User, Tutor

class TutorModelTestCase(TestCase):
    """Unit tests for the Tutor model."""

    def setUp(self):

        # Create a User instance
        user = User.objects.create_user(
            username='@testtutor',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Tutor',
            email='testtutor@example.com',
        )

        # Create the associated Student instance
        self.tutor = Tutor.objects.create(user=user, rate=25.00, specializes_in_python=True, available_monday=True)

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
        tutor_without_specialties = User.objects.create(
            username='@newtutor',
            password=make_password('Password123'),
            first_name='New',
            last_name='Tutor',
            email='newtutor@example.com',
        )
        self.tutor_wo_s = Tutor.objects.create(user=tutor_without_specialties, rate=25.00)
        self.assertEqual(self.tutor_wo_s.get_specialties(), [])

    def test_default_availability(self):
        """Test default values for availability (should be False)."""
        tutor_without_availability = User.objects.create(
            username='@tutorwithoutavailability',
            password=make_password('Password123'),
            first_name='No',
            last_name='Availability',
            email='noavailability@example.com',
        )
        self.tutor_wo_a = Tutor.objects.create(user=tutor_without_availability, rate=25.00)
        self.assertEqual(self.tutor_wo_a.get_availability(), [])

    def test_rate_validation(self):
        """Test rate field validation (should not be negative)."""
        tutor_user = User.objects.create_user(
            username='@invalidrate',
            password='Password123',
            first_name='Invalid',
            last_name='Rate',
            email='invalidrate@example.com',
        )

        # Create a Tutor with a negative rate
        tutor_with_invalid_rate = Tutor(user=tutor_user, rate=-10.00)

        # Validation should fail when full_clean is called
        with self.assertRaises(ValidationError):
            tutor_with_invalid_rate.full_clean()


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
