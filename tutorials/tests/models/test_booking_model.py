from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from tutorials.models.booking_model import Booking
from tutorials.models.student_model import Student
from tutorials.models.user_models import User
from django.contrib.auth.hashers import make_password

class BookingModelTestCase(TestCase):
    """Unit tests for the Booking model."""

    def setUp(self):

        student_user = User.objects.create_user(
            username='@teststudent',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
        )

        self.student = Student.objects.create(user=student_user, level='BEGINNER')


        self.booking = Booking.objects.create(
            student = self.student,
            date="2024-12-02",  #YYYY-MM-DD format
            time="14:30:00",    #HH:MM:SS format
            frequency="weekly",
            duration="short",
            day = "Tuesday",
            lang = "C"
        )

    def test_valid_booking(self):
        self._assert_booking_is_valid()

    def test_booking_str(self):
        expected_str = f"Requested: Booking for {self.student} on 2024-12-02 at 14:30:00"
        self.assertEqual(str(self.booking), expected_str)

    #tests for date
    def test_date_cannot_be_empty(self):
        self.booking.date = ""
        self._assert_booking_is_invalid()

    def test_date_must_have_three_fields(self):
        self.booking.date = "2024-12-05-19"
        self._assert_booking_is_invalid()

    def test_date_must_be_existing(self):
        self.booking.date = "2024-12-34"
        self._assert_booking_is_invalid()

    def test_date_must_have_dashes(self):
        self.booking.date = "20241201"
        self._assert_booking_is_invalid()

    def test_date_must_have_correct_order(self):
        self.booking.date = "01-01-2024"
        self._assert_booking_is_invalid()

    def test_date_autocorrects_to_eight_digits(self):
        self.booking.date = "2024-12-1"
        self._assert_booking_is_valid()

    def test_year_must_be_four_digits(self):
        self.booking.date = "202-12-1"
        self._assert_booking_is_invalid()


    #tests for time
    def test_time_cannot_be_empty(self):
        self.booking.time = ""
        self._assert_booking_is_invalid()

    def test_time_must_have_three_fields(self):
        self.booking.time = "14:30:00:12"
        self._assert_booking_is_invalid()

    def test_time_must_be_existing(self):
        self.booking.time = "73:30:00"
        self._assert_booking_is_invalid()

    def test_time_must_have_colons(self):
        self.booking.time = "143000"
        self._assert_booking_is_invalid()

    def test_time_autocorrects_to_six_digits(self):
        self.booking.time = "14:30:9"
        self._assert_booking_is_valid()


    #tests for frequency
    def test_frequency_cannot_be_empty(self):
        self.booking.frequency = ""
        self._assert_booking_is_invalid()

    def test_frequency_must_be_valid_choice(self):
        self.booking.frequency = "never"
        self._assert_booking_is_invalid()

    def test_frequency_weekly_valid(self):
        self.booking.frequency = "weekly"
        self._assert_booking_is_valid()

    def test_frequency_fortnightly_valid(self):
        self.booking.frequency = "fortnightly"
        self._assert_booking_is_valid()

    def test_frequency_max_length_twenty(self):
        self.booking.frequency = "fortnightly                   "
        self._assert_booking_is_invalid()


    #tests for duration
    def test_duration_cannot_be_empty(self):
        self.booking.duration = ""
        self._assert_booking_is_invalid()

    def test_duration_must_be_valid_choice(self):
        self.booking.duration = "forever"
        self._assert_booking_is_invalid()

    def test_duration_weekly_valid(self):
        self.booking.duration = "short"
        self._assert_booking_is_valid()

    def test_duration_fortnightly_valid(self):
        self.booking.duration = "long"
        self._assert_booking_is_valid()

    def test_duration_max_length_ten(self):
        self.booking.duration = "short               "
        self._assert_booking_is_invalid()

    def test_display_to_user_short(self):
        self.booking.duration = "short"
        self.assertEqual(self.booking.get_duration_display(), "short (1hr)")

    def test_display_to_user_long(self):
        self.booking.duration = "long"
        self.assertEqual(self.booking.get_duration_display(), "long (2hrs)")


    #tests for student (foreign key)
    def test_booking_deleted_when_student_deleted(self):
        self.booking.student.delete()
        with self.assertRaises(Booking.DoesNotExist):
            Booking.objects.get(id=self.booking.id)

    def test_student_related_name_for_bookings(self):
        bookings = self.student.bookings.all()
        self.assertEqual(bookings.count(), 1)

    def test_invalid_student_foreign_key(self):
        invalid_student = Student.objects.filter(user__id=999).first()
        self.booking.student = invalid_student
        self._assert_booking_is_invalid()

    def test_default_foreign_key_value(self):
        default_student = Student.objects.filter(user__id=1).first()
        self.booking = Booking.objects.create(
            date="2024-12-01",  #YYYY-MM-DD format
            time="14:30:00",    #HH:MM:SS format
            frequency="weekly",
            duration="short"
        )
        self.assertEqual(self.booking.student, default_student)


    #tests for day
    def test_day_can_be_monday(self):
        self.booking.day = "Monday"
        self._assert_booking_is_valid()

    def test_day_can_be_tuesday(self):
        self.booking.day = "Tuesday"
        self._assert_booking_is_valid()

    def test_day_can_be_wednesday(self):
        self.booking.day = "Wednesday"
        self._assert_booking_is_valid()

    def test_day_can_be_thursday(self):
        self.booking.day = "Thursday"
        self._assert_booking_is_valid()

    def test_day_can_be_friday(self):
        self.booking.day = "Friday"
        self._assert_booking_is_valid()

    def test_day_cannot_be_invalid(self):
        self.booking.day = "Saturday"
        self._assert_booking_is_invalid()

    def test_day_cannot_be_blank(self):
        self.booking.day = ""
        self._assert_booking_is_invalid()


    #tests for language
    def test_lang_can_be_java(self):
        self.booking.lang = "Java"
        self._assert_booking_is_valid()

    def test_lang_can_be_ruby(self):
        self.booking.lang = "Ruby"
        self._assert_booking_is_valid()

    def test_lang_can_be_C(self):
        self.booking.lang = "C"
        self._assert_booking_is_valid()

    def test_lang_can_be_SQL(self):
        self.booking.lang = "SQL"
        self._assert_booking_is_valid()

    def test_lang_can_be_python(self):
        self.booking.lang = "Python"
        self._assert_booking_is_valid()

    def test_lang_cannot_be_invalid(self):
        self.booking.lang = "Pascal"
        self._assert_booking_is_invalid()

    def test_lang_cannot_be_blank(self):
        self.booking.lang = ""
        self._assert_booking_is_invalid()

    
    #tests for status
    def test_status_cannot_be_empty(self):
        self.booking.status = ""
        self._assert_booking_is_invalid()

    def test_status_can_be_open(self):
        self.booking.status = "OPEN"
        self._assert_booking_is_valid()
    
    def test_status_can_be_closed(self):
        self.booking.status = "CLOSED"
        self._assert_booking_is_valid()

    def test_status_must_be_valid_choice(self):
        self.booking.status = "IN REVIEW"
        self._assert_booking_is_invalid()

    def test_status_max_length_ten(self):
        self.booking.status = "OPEN          "
        self._assert_booking_is_invalid()

    #helper methods
    def _assert_booking_is_valid(self):
        try:
            self.booking.full_clean()
        except (ValidationError):
            self.fail('Booking should be valid')

    def _assert_booking_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.booking.full_clean()

