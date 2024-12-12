from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from tutorials.models.tutor_model import Tutor
from tutorials.models.student_model import Student
from tutorials.models.booking_model import Booking
from tutorials.models.lesson_model import Lesson
from tutorials.models.user_models import User
from tutorials.forms.lesson_forms import AssignTutorForm
from tutorials.forms.booking_forms import BookingForm
from datetime import date, datetime, time
from django.contrib.auth.hashers import make_password

class AssignTutorViewTest(TestCase):
    def setUp(self):
        #create sample tutors for testing
        user = User.objects.create_user(
            username='@testtutor',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Tutor',
            email='testtutor@example.com',
            role = "tutor",
        )
        self.tutor_1 = Tutor.objects.create(
            user=user,
            specializes_in_python=True,
            specializes_in_c=True,
            available_monday=True,
            available_tuesday=True,
            rate=9.00,  # Hourly rate in the preferred currency
        )

        user2 = User.objects.create_user(
            username='@testtutor2',
            password=make_password('Password123'),
            first_name='Test2',
            last_name='Tutor2',
            email='testtutor2@example.com',
            role = "tutor"
        )

        self.tutor_2 = Tutor.objects.create(
            user=user2,
            specializes_in_c=True,
            available_monday=True,
            available_wednesday=True,
            rate=10.00,  # Hourly rate in the preferred currency
        )

        user3 = User.objects.create_user(
            username='@teststudent',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
            role = "student"
        )

        self.student = Student.objects.create(
            user = user3,
            level='BEGINNER'
        )

        self.booking = Booking.objects.create(
            student = self.student,
            date="2025-01-06",  #YYYY-MM-DD format
            time="14:30:00",    #HH:MM:SS format
            frequency="weekly",
            duration="short",
            day = "Monday",
            lang = "Python",
            status = "OPEN"
        )
        self.url = reverse("assign_tutor", args=[self.booking.id])

    def test_view_renders_correct_template(self):
        #test the view renders the correct template with expected context
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assign_tutor.html")
        self.assertIn("assign_form", response.context)
        self.assertIn("booking_form", response.context)
        self.assertIn("no_tutors", response.context)

    def test_view_filters_tutors_correctly(self):
        #test that tutors are filtered based on booking language and day
        response = self.client.get(self.url)
        assign_form = response.context["assign_form"]
        self.assertEqual(list(assign_form.fields["tutor"].queryset), [self.tutor_1])
    
    def test_save_changes_updates_booking(self):
        #test that 'save_changes' correctly updates the booking details
        updated_time = "15:30"
        response = self.client.post(self.url, {
            "save_changes": "",
            "date": "2025-01-06",
            "time": updated_time,
            "frequency": "weekly",
            "duration": "short",
            "day": "Monday",
            "lang": "Python",
            "status" : "OPEN"
        })
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.time.strftime("%H:%M"), updated_time)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Booking details updated successfully!", messages)

    def test_assign_tutor_creates_lessons(self):
        #test that 'assign_tutor' creates lessons and deletes the booking
        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": self.tutor_1.user_id,
        })

        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())  # Booking is deleted
        lessons = Lesson.objects.filter(tutor=self.tutor_1)
        self.assertTrue(lessons.exists())
        self.assertEqual(lessons.first().booking.date.strftime("%Y-%m-%d"), self.booking.date)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Tutor assigned successfully and further lessons booked!", messages)

    def test_assign_tutor_handles_overlapping_lessons(self):
        #test that overlapping lessons prevent a tutor assignment
        Lesson.objects.create(
            booking=self.booking,
            tutor=self.tutor_1,
        )
        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": self.tutor_1.user_id,
        })

        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())  #booking is not deleted
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("This tutor is already booked for an overlapping lesson.", messages)

    def test_assign_tutor_invalid_form(self):
        #test that an invalid AssignTutorForm does not create lessons
        r = self.client.post(self.url, {
            "save_changes": "",
            "date": "2025-01-06",
            "time": "14:30:00",
            "frequency": "weekly",
            "duration": "short",
            "day": "Monday",
            "lang": "Python",
            "status" : "OPEN"
        })
        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": 999,  #nonexistent tutor
        })

        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())  #booking is not deleted
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Select a valid choice. That choice is not one of the available choices.", response.content.decode())

    def test_invalid_booking_form(self):
        #test that an invalid BookingForm does not update the booking
        response = self.client.post(self.url, {
            "save_changes": "",
            "date": "",  #invalid date
        })
        self.assertEqual(self.booking.date, "2025-01-06")  #booking date remains unchanged
        self.assertContains(response, "This field is required.")  #error is displayed in the form

    def test_no_tutors_available(self):
        #test that the context indicates no tutors available when none match
        self.booking.lang = "Ruby"
        self.booking.save()

        response = self.client.get(self.url)
        self.assertTrue(response.context["no_tutors"])
    
    def test_error_handling_for_missing_booking(self):
        #test that a 404 error is raised if the booking does not exist
        non_existent_url = reverse("assign_tutor", args=[9999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 404)
    