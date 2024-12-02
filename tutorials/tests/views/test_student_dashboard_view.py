from django.test import TestCase
from django.urls import reverse

#TODO: Update depending on how models are implemented

class StudentDashboardViewTest(TestCase):
    def setUp(self):
        # Setup sample data (e.g., create lessons and invoices)
        self.upcoming_lessons = [
            {
                'date': '2024-12-05',
                'time': '10:00 AM',
                'duration': '1 hour',
                'tutor': 'John Doe',
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

    def test_dashboard_view_context(self):
        response = self.client.get(reverse('student_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('upcoming_lessons', response.context)
        self.assertIn('previous_lessons', response.context)
        self.assertIn('invoices', response.context)
