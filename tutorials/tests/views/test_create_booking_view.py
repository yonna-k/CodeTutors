from django.test import TestCase
from django.urls import reverse
from tutorials.forms.booking_forms import BookingForm
from tutorials.models.booking_model import Booking
from tutorials.models.student_model import Student
from tutorials.models.user_models import User
from tutorials.models.tutor_model import Tutor
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages

class CreateBookingViewTestCase(TestCase):
    fixtures = [
        'tutorials/tests/fixtures/default_user.json',
        'tutorials/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.student_user = User.objects.create_user(
            username='studentuser',
            password='Password123',
            first_name='Student',
            last_name='User',
            email='studentuser@example.com',
            role='student',
        )
        self.student = Student.objects.create(user=self.student_user, level='BEGINNER')

        # Create a tutor user
        self.tutor_user = User.objects.create_user(
            username='tutoruser',
            password='Password123',
            first_name='Tutor',
            last_name='User',
            email='tutoruser@example.com',
            role='tutor',
        )
        self.tutor = Tutor.objects.create(user=self.tutor_user, rate=20.00)

        # URL for booking form
        self.url = reverse('create_booking')

        # Sample valid booking data
        self.valid_data = {
            'student': self.student.user_id,
            'time': '14:30:00',
            'duration': 'short',
            'frequency': 'weekly',
            'day': 'Monday',
            'lang': 'Python',
        }

    def test_get_create_booking(self):
        """Test that the create booking page is accessible to authorized users."""
        self.client.login(username=self.student_user.username, password='Password123')  # Ensure the user is logged in
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_session.html')  # Updated template name

    def test_post_valid_as_student(self):
        self.client.login(username=self.student_user.username, password='Password123')  # Ensure the user is logged in
        prev_count = Booking.objects.count()
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, reverse('student_dashboard'))
        self.assertEqual(Booking.objects.count(), prev_count + 1)

    def test_post_invalid_as_non_student(self):
        self.client.login(username=self.tutor_user.username, password='Password123')  # Ensure the user is logged in
        prev_count = Booking.objects.count()
        response = self.client.post(self.url, data=self.valid_data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Booking.objects.count(), prev_count)
