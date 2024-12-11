from django.test import TestCase
from tutorials.models import User, Student, Tutor, Booking, Lesson
from datetime import date, time

#TODO: Add more tests

class EntityDeleteTestCase(TestCase):
    """Test cases for the `delete_*` views."""

    def setUp(self):
        # Create a User instance
        self.user = User.objects.create_user(
            username="@testuser",
            first_name="Test",
            last_name="User",
            email="test.user@example.com",
            role="student"
        )

        # Create a Student instance linked to the User
        self.student = Student.objects.create(user=self.user, level="BEGINNER")

        # Create a Tutor instance with specialties and availability
        self.tutor_user = User.objects.create_user(
            username="@tutoruser",
            first_name="Tutor",
            last_name="User",
            email="tutor.user@example.com",
            role="tutor"
        )
        self.tutor = Tutor.objects.create(
            user=self.tutor_user,
            specializes_in_python=True,
            available_monday=True,
            rate=50.00
        )

        # Create a Booking instance for the Student
        self.booking = Booking.objects.create(
            student=self.student,
            date=date.today(),
            time=time(10, 0),
            frequency="weekly",
            duration="short",
            day="Monday",
            lang="Python"
        )

        # Create a Lesson instance linked to the Booking and Tutor
        self.lesson = Lesson.objects.create(booking=self.booking, tutor=self.tutor)

    def tearDown(self):
        # Clean up after each test
        User.objects.all().delete()
        Student.objects.all().delete()
        Tutor.objects.all().delete()
        Booking.objects.all().delete()
        Lesson.objects.all().delete()