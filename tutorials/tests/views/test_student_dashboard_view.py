from django.test import TestCase
from django.urls import reverse
from tutorials.models.user_models import User

#TODO: Update depending on how models are implemented

class StudentDashboardViewTest(TestCase):
    """Tests of the student dashboard view."""

    fixtures = [
            'tutorials/tests/fixtures/default_user.json',
            'tutorials/tests/fixtures/other_users.json'
        ]

    def setUp(self):

        self.url = reverse('student_dashboard')
        self.user = User.objects.get(username='@charlie')

    def test_student_dashboard_url(self):
        self.assertEqual(self.url, '/dashboard/student/')

    def test_get_dashboard_view(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')

        self.assertIn('previous_lessons', response.context)
        self.assertIn('upcoming_lessons', response.context)

        previous_lessons = response.context['previous_lessons']
        upcoming_lessons = response.context['upcoming_lessons']

        self.assertEqual(previous_lessons.count(), 0)  # No previous lessons
        self.assertEqual(upcoming_lessons.count(), 1)  # One upcoming lesson
        lesson = upcoming_lessons.first()
        self.assertEqual(lesson.booking.student.user.username, '@charlie')
    
    #TODO: Test redirect for when Student logs in
    def test_get_home_redirects_when_logged_in(self):
        pass

    #TODO: Tests for buttons on the page for checking bookings
