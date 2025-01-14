from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from tutorials.models.lesson_model import Lesson
from tutorials.models.booking_model import Booking
from tutorials.models.student_model import Student
from tutorials.models.tutor_model import Tutor
from tutorials.models.user_models import User
from django.contrib.auth.hashers import make_password

class LessonModelTest(TestCase):
    def setUp(self):

        student_user = User.objects.create_user(
            username='@teststudent',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
        )

        self.student = Student.objects.create(user=student_user, level='BEGINNER')

        tutor_user = User.objects.create_user(
            username="@testtutor",
            password=make_password('Password123'),
            first_name="Test",
            last_name="Tutor",
            email="testtutor@example.com",
        )

        # Create the associated Student instance
        self.tutor = Tutor.objects.create(user=tutor_user,
            specializes_in_python=True,
            specializes_in_java=False,
            specializes_in_c=True,
            specializes_in_ruby=False,
            specializes_in_sql=True,
            available_monday=True,
            available_tuesday=True,
            available_wednesday=False,
            available_thursday=True,
            available_friday=True,
            available_saturday=False,
            available_sunday=False,
            rate=9.00,)


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
        expected_str = (
        f"Lesson on {self.booking.date} at {self.booking.time} "
        f"with Tutor {self.tutor.user.first_name}, costing {self.lesson.invoice}"
        )
        self.assertEqual(str(self.lesson), expected_str)


    def test_lesson_deletes_when_booking_deletes(self):
        self.booking.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(booking_id=self.lesson.booking_id)

    def test_lesson_deletes_when_tutor_deletes(self):
        self.tutor.delete()
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(booking_id=self.lesson.booking_id)

    def test_invalid_booking_foreign_key(self):
        invalid_booking = Booking.objects.filter(id=999).first()
        self.lesson.booking = invalid_booking
        self._assert_lesson_is_invalid()

    def test_invalid_tutor_foreign_key(self):
        invalid_tutor = Tutor.objects.filter(user_id=999).first()
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

    def test_invoice_calculated_when_tutor_rate_is_zero(self):
        self.tutor.rate = 0
        self.tutor.save()
        
        self.assertEqual(self.lesson.invoice, 0)


    #helper methods
    def _assert_lesson_is_valid(self):
        try:
            self.lesson.full_clean()
        except ValidationError:
            self.fail('Lesson should be valid')

    def _assert_lesson_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.lesson.full_clean()
