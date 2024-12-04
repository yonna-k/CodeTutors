from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from tutorials.models.lesson_models import Lesson
from tutorials.models.booking_models import Booking
from tutorials.models.student_models import Student
from tutorials.models.tutor_model import Tutor
from django.contrib.auth.hashers import make_password

class LessonModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            username='@teststudent',
            password=make_password('Password123'), 
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
            level='BEGINNER'
        )

        self.tutor = Tutor.objects.create(
            username="@testtutor",
            password=make_password('Password123'),
            first_name="Test",
            last_name="Tutor",
            email="testtutor@example.com",
            specializes_in_python=True,
            specializes_in_java=False,
            specializes_in_C=True,
            specializes_in_ruby=False,
            specializes_in_SQL=True,
            available_monday=True,
            available_tuesday=True,
            available_wednesday=False,
            available_thursday=True,
            available_friday=True,
            available_saturday=False,
            available_sunday=False,
            rate=9.00,  # Hourly rate in the preferred currency
        )

        self.booking = Booking.objects.create(
            student = self.student,
            date="2024-12-02",  #YYYY-MM-DD format
            time="14:30:00",    #HH:MM:SS format
            frequency="weekly",
            duration="short",
            day = "Tuesday",
            lang = "C"
        )

        self.lesson = Lesson.objects.create(
            booking=self.booking,
            tutor=self.tutor
        )

    def test_valid_lesson(self):
        self._assert_lesson_is_valid()

    def test_lesson_str(self):
        expected_str = f"Lesson on {self.booking.date} at {self.booking.time} with Tutor {self.tutor.first_name}, costing {self.lesson.invoice}"
        self.assertEqual(str(self.lesson), expected_str)

    def test_lesson_deletes_when_booking_deletes(self):
        self.booking.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)
    
    def test_lesson_deletes_when_tutor_deletes(self):
        self.tutor.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=self.lesson.id)

    def test_invalid_booking_foreign_key(self):
        invalid_booking = Booking.objects.filter(id=999).first()
        self.lesson.booking = invalid_booking
        self._assert_lesson_is_invalid()
    
    def test_invalid_tutor_foreign_key(self):
        invalid_tutor = Tutor.objects.filter(id=999).first()
        self.lesson.tutor = invalid_tutor
        self._assert_lesson_is_invalid()
    
    def test_booking_can_have_only_one_lesson(self):
        with self.assertRaises(IntegrityError):
            Lesson.objects.create(
                booking=self.booking,
                tutor=self.tutor
            )

    def test_valid_tutor_relationship(self):
        self.lesson.tutor = self.tutor
        self._assert_lesson_is_valid()

    def test_invoice_calculated_correctly_short(self):
        #map duration to integer value
        DURATION_MULTIPLIER = {
            "short": 1,
            "long": 2,
        }
        self.assertEqual(DURATION_MULTIPLIER.get(self.lesson.booking.duration, 1) * self.lesson.tutor.rate, self.lesson.invoice)

    def test_invoice_calculated_correctly_long(self):
        #map duration to integer value
        DURATION_MULTIPLIER = {
            "short": 1,
            "long": 2,
        }
        self.lesson.booking.duration = "long"
        self.assertEqual(DURATION_MULTIPLIER.get(self.lesson.booking.duration, 1) * self.lesson.tutor.rate, self.lesson.invoice)


    #helper methods
    def _assert_lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except ValidationError:
            self.fail('Lesson should be valid')

    def _assert_lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()