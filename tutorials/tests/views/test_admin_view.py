from django.test import TestCase
from tutorials.models import User, Student, Tutor, Booking, Lesson, Admin
from datetime import date, time
from django.urls import reverse
from django.contrib.auth.hashers import make_password

class AdminViewTestCase(TestCase):
    fixtures = ['tutorials/tests/fixtures/default_user.json', 'tutorials/tests/fixtures/other_users.json']

    def setUp(self):
        self.admin = User.objects.get(pk=1)
        self.tutor = User.objects.get(pk=2)
        self.student = User.objects.get(pk=3)

        self.client.force_login(self.admin)
    
    def test_manage_users_view(self):
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_users.html')
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), User.objects.count())

    def test_manage_students_view(self):
        response = self.client.get(reverse('manage_students'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_students.html')
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), Student.objects.count())
    
    def test_manage_tutors_view(self):
        response = self.client.get(reverse('manage_tutors'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_tutors.html')
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), Tutor.objects.count())

    def test_manage_admins_view(self):
        response = self.client.get(reverse('manage_admins'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_admins.html')
        self.assertIn('users', response.context)
        self.assertEqual(len(response.context['users']), Admin.objects.count())
    
    def test_manage_bookings_view(self):
        response = self.client.get(reverse('manage_bookings'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_bookings.html')
        self.assertIn('bookings', response.context)
        self.assertEqual(len(response.context['bookings']), Booking.objects.filter(status="OPEN").count())

    def test_manage_lessons_view(self):
        response = self.client.get(reverse('manage_lessons'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manage/manage_lessons.html')
        self.assertIn('lessons', response.context)
        self.assertEqual(len(response.context['lessons']), Lesson.objects.count())

    def test_get_user_view(self):
        response = self.client.get(reverse('get_user', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/user.html')
        self.assertEqual(response.context['user'], self.student)

    def test_get_student_view(self):
        student = Student.objects.get(user=self.student)
        response = self.client.get(reverse('get_student', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/student.html')
        self.assertEqual(response.context['student'], student)

    def test_get_tutor_view(self):
        tutor = Tutor.objects.get(user=self.tutor)
        response = self.client.get(reverse('get_tutor', args=[self.tutor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/tutor.html')
        self.assertEqual(response.context['tutor'], tutor)

    def test_get_admin_view(self):
        admin = Admin.objects.get(user=self.admin)
        response = self.client.get(reverse('get_admin', args=[self.admin.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/admin-profile.html')
        self.assertEqual(response.context['admin'], admin)

    def test_get_booking_view(self):
        booking = Booking.objects.get(pk=2)
        response = self.client.get(reverse('get_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/booking.html')
        self.assertEqual(response.context['booking'], booking)

    def test_get_lesson_view(self):
        lesson = Lesson.objects.get(pk=1)
        response = self.client.get(reverse('get_lesson', args=[lesson.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/lesson.html')
        self.assertEqual(response.context['lesson'], lesson)

    def test_delete_user_view(self):
        response = self.client.post(reverse('delete_user', args=[self.tutor.id]))
        self.assertRedirects(response, reverse('manage_users'))
        self.assertFalse(User.objects.filter(pk=self.tutor.id).exists())

    def test_delete_student_view(self):
        student = Student.objects.get(user=self.student)
        response = self.client.post(reverse('delete_student', args=[self.student.id]))
        self.assertRedirects(response, reverse('manage_students'))
        self.assertFalse(Student.objects.filter(pk=student.user_id).exists())

    def test_delete_tutor_view(self):
        tutor = Tutor.objects.get(user=self.tutor)
        response = self.client.post(reverse('delete_tutor', args=[self.tutor.id]))
        self.assertRedirects(response, reverse('manage_tutors'))
        self.assertFalse(Tutor.objects.filter(pk=tutor.user_id).exists())

    def test_delete_admin_view(self):
        admin = Admin.objects.get(user=self.admin)
        response = self.client.post(reverse('delete_admin', args=[self.admin.id]))
        self.assertRedirects(response, reverse('manage_admins'))
        self.assertFalse(Admin.objects.filter(pk=admin.user_id).exists())

    def test_delete_booking_view(self):
        booking = Booking.objects.get(pk=2)
        response = self.client.post(reverse('delete_booking', args=[booking.id]))
        self.assertRedirects(response, reverse('manage_bookings'))
        self.assertFalse(Booking.objects.filter(pk=booking.id).exists())

    def test_delete_lesson_view(self):
        lesson = Lesson.objects.get(pk=1)
        response = self.client.post(reverse('delete_lesson', args=[lesson.booking.id]))
        self.assertRedirects(response, reverse('manage_lessons'))
        self.assertFalse(Lesson.objects.filter(pk=lesson.booking_id).exists())