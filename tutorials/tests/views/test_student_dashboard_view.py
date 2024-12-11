from django.test import TestCase
from django.urls import reverse
from tutorials.models.user_models import User

#TODO: Update depending on how models are implemented

class StudentDashboardViewTest(TestCase):
    """Tests of the student dashboard view."""

    # TODO: maybe add @charlie (who is a student) to the fixtures to avoid using @johndoe
    fixtures = ['tutorials/tests/fixtures/default_user.json']

    def setUp(self):
        # Setup sample data (e.g., create lessons and invoices)
        self.url = reverse('student_dashboard')
        self.user = User.objects.get(username='@johndoe')

        self.upcoming_lessons = [
            {
                'date': '2024-12-05',
                'time': '10:00 AM',
                'duration': '1 hour',
                'tutor': 'John Smith',
                'subject': 'Mathematics',
                'venue': 'Room 101'
            }
        ]
        self.previous_lessons = [
            {
                'date': '2024-11-20',
                'time': '09:00 AM',
                'duration': '1 hour',
                'tutor': 'Jane Smith',
                'subject': 'Physics',
            }
        ]
        self.invoices = [
            {
                'number': 'INV001',
                'term': 'Fall 2024',
                'amount': '£100',
                'status': 'Paid',
            }
        ]

    def test_student_dashboard_url(self):
        self.assertEqual(self.url,'/dashboard/student/')

    def test_get_dashboard_view(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_dashboard.html')
    
    #TODO: Test redirect for when Student logs in
    # def test_get_home_redirects_when_logged_in(self):
    #     self.client.login(username=self.user.username, password="Password123")
    #     response = self.client.get(self.url, follow=True)
    #     redirect_url = reverse('student_dashboard')
    #     self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
    #     self.assertTemplateUsed(response, 'student_dashboard.html')

    #TODO: Tests for buttons on the page for checking bookings
