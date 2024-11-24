from django.test import TestCase
from django.urls import reverse
from tutorials.forms.booking_forms import BookingForm
from tutorials.models.booking_models import Booking
from tutorials.models.student_models import Student
from tutorials.models.user_models import User
from django.contrib.auth.hashers import make_password
from django.contrib.messages import get_messages

class CreateBookingViewTestCase(TestCase):

    fixtures = [
        'tutorials/tests/fixtures/default_user.json',
        'tutorials/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        # Create a student and a user
        self.student = Student.objects.create(
            username='@teststudent',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
            level='BEGINNER'
        )
        
        self.user = User.objects.get(username='@johndoe')
        

        # URL for booking form
        self.url = reverse('create_booking')  # Make sure the URL name is correct

        # Sample valid booking data
        self.valid_data = {
            'date': '2025-02-12', 
            'time': '14:30:00',
            'frequency': 'weekly',
            'duration': 'short'
        }

    def test_get_create_booking(self):
        self.client.login(username='@teststudent', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'book_session.html')

    def test_post_valid_as_student(self):
        self.client.login(username='@teststudent', password='Password123')
        prev_count = Booking.objects.count()
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Booking.objects.count(), prev_count + 1)

    def test_post_invalid_as_non_student(self):
        self.client.login(username='@johndoe', password='Password123')
        prev_count = Booking.objects.count()
        response = self.client.post(self.url, data=self.valid_data)
        self.assertRedirects(response, reverse('dashboard'))
        self.assertEqual(Booking.objects.count(), prev_count)