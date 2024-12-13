from django.test import TestCase
from django.urls import reverse
from django.contrib.messages import get_messages
from tutorials.models.tutor_model import Tutor
from tutorials.models.student_model import Student
from tutorials.models.booking_model import Booking
from tutorials.models.lesson_model import Lesson
from tutorials.models.user_models import User

class AssignTutorViewTest(TestCase):
    fixtures = [
        'tutorials/tests/fixtures/other_users.json',
        'tutorials/tests/fixtures/default_user.json',
    ]

    def setUp(self):
        self.admin_user = User.objects.get(pk=1)
        self.client.login(username=self.admin_user.username, password='Password123')

        self.tutor = Tutor.objects.get(pk=2) # @janedoe
        self.booking = Booking.objects.get(pk=11) # unassigned booking by @peterpickle
        self.url = reverse("assign_tutor", args=[self.booking.id])


    def test_view_renders_correct_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assign_tutor.html")
        self.assertIn("assign_form", response.context)
        self.assertIn("booking_form", response.context)
        self.assertIn("no_tutors", response.context)

    def test_view_filters_tutors_correctly(self):
        response = self.client.get(self.url)
        assign_form = response.context["assign_form"]
        self.assertEqual(list(assign_form.fields["tutor"].queryset), [self.tutor])

    def test_save_changes_updates_booking(self):
        updated_time = "15:30"
        response = self.client.post(self.url, {
            "save_changes": "",
            "date": "2025-01-06",
            "time": updated_time,
            "frequency": "weekly",
            "duration": "short",
            "day": "Monday",
            "lang": "Python",
            "status": "OPEN"
        })

        self.booking.refresh_from_db()
        self.assertEqual(self.booking.time.strftime("%H:%M"), updated_time)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Booking details updated successfully!", messages)

    def test_assign_tutor_creates_lessons(self):
        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": self.tutor.user_id,
        })

        self.assertFalse(Booking.objects.filter(id=self.booking.id).exists())

        lessons = Lesson.objects.filter(tutor=self.tutor)

        self.assertTrue(lessons.exists())

        lesson_matched = False

        for lesson in lessons:
            try:
                self.assertEqual(lesson.booking.student, self.booking.student)
                self.assertEqual(lesson.booking.lang, self.booking.lang)
                self.assertEqual(lesson.booking.time, self.booking.time)
                self.assertEqual(lesson.booking.day, self.booking.day)
                
                self.assertTrue(lesson.booking.date >= self.booking.date)

                lesson_matched = True
                break

            except AssertionError:
                continue
        
        self.assertTrue(lesson_matched, "No lesson met the required criteria")

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("Tutor assigned successfully and further lessons booked!", messages)


    def test_assign_tutor_handles_overlapping_lessons(self):
        Lesson.objects.create(
            booking=self.booking,
            tutor=self.tutor,
        )

        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": self.tutor.user_id,
        })

        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn("This tutor is already booked for an overlapping lesson.", messages)

    def test_assign_tutor_invalid_form(self):
        response = self.client.post(self.url, {
            "assign_tutor": "",
            "tutor": 999,  # Nonexistent tutor
        })

        self.assertFormError(response, 'assign_form', 'tutor', 'Select a valid choice. That choice is not one of the available choices.')
        self.assertTrue(Booking.objects.filter(id=self.booking.id).exists())

    def test_invalid_booking_form(self):
        response = self.client.post(self.url, {
            "save_changes": "",
            "date": "",  # Invalid date
        })
        self.booking.refresh_from_db()
        self.assertNotEqual(self.booking.date, "")  # Booking date remains unchanged
        self.assertContains(response, "This field is required.")

    def test_no_tutors_available(self):
        Tutor.objects.all().delete()

        response = self.client.get(self.url)
        self.assertIn("no_tutors", response.context)
        self.assertTrue(response.context["no_tutors"])

    def test_error_handling_for_missing_booking(self):
        non_existent_url = reverse("assign_tutor", args=[9999])
        response = self.client.get(non_existent_url)
        self.assertEqual(response.status_code, 404)