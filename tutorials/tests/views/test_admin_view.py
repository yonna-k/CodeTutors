from sqlite3 import IntegrityError
from django.http import Http404
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

    def test_get_user_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_user', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_get_student_view(self):
        student = Student.objects.get(user=self.student)
        response = self.client.get(reverse('get_student', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/student.html')
        self.assertEqual(response.context['student'], student)

    def test_get_student_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_student', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_get_tutor_view(self):
        tutor = Tutor.objects.get(user=self.tutor)
        response = self.client.get(reverse('get_tutor', args=[self.tutor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/tutor.html')
        self.assertEqual(response.context['tutor'], tutor)

    def test_get_tutor_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_tutor', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_get_admin_view(self):
        admin = Admin.objects.get(user=self.admin)
        response = self.client.get(reverse('get_admin', args=[self.admin.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/admin-profile.html')
        self.assertEqual(response.context['admin'], admin)

    def test_get_admin_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_admin', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_get_booking_view(self):
        booking = Booking.objects.get(pk=11)
        response = self.client.get(reverse('get_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/booking.html')
        self.assertEqual(response.context['booking'], booking)

    def test_get_booking_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_booking', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_get_lesson_view(self):
        lesson = Lesson.objects.get(pk=10)
        response = self.client.get(reverse('get_lesson', args=[lesson.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/lesson.html')
        self.assertEqual(response.context['lesson'], lesson)

    def test_get_lesson_view_not_found(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('get_lesson', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_user_view(self):
        response = self.client.post(reverse('delete_user', args=[self.tutor.id]))
        self.assertRedirects(response, reverse('manage_users'))
        self.assertFalse(User.objects.filter(pk=self.tutor.id).exists())

    def test_delete_invalid_user(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_user', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_student_view(self):
        student = Student.objects.get(user=self.student)
        response = self.client.post(reverse('delete_student', args=[self.student.id]))
        self.assertRedirects(response, reverse('manage_students'))
        self.assertFalse(Student.objects.filter(pk=student.user_id).exists())

    def test_delete_invalid_student(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_student', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_tutor_view(self):
        tutor = Tutor.objects.get(user=self.tutor)
        response = self.client.post(reverse('delete_tutor', args=[self.tutor.id]))
        self.assertRedirects(response, reverse('manage_tutors'))
        self.assertFalse(Tutor.objects.filter(pk=tutor.user_id).exists())

    def test_delete_invalid_tutor(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_tutor', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_self_admin_view(self):
        response = self.client.post(reverse('delete_admin', args=[self.admin.id]))
        self.assertEqual(response.status_code, 403) # can't delete yourself
        self.assertTrue(Admin.objects.filter(user=self.admin).exists())
    
    def test_delete_admin_view(self):
        self.second_admin_user = User.objects.create_user(
            username='test_admin2', 
            email='admin2@example.com', 
            password='password123',
            first_name='Test', 
            last_name='Admin'
        )
        self.second_admin_user.role = 'admin' 
        self.second_admin_user.save()
        self.second_admin = Admin.objects.create(user=self.second_admin_user)
        self.second_admin.save()
        
        second_admin = Admin.objects.get(user=self.second_admin_user)
        response = self.client.post(reverse('delete_admin', args=[second_admin.user_id]))
        self.assertRedirects(response, reverse('manage_admins'))
        self.assertFalse(Admin.objects.filter(pk=second_admin.user.id).exists())

    def test_delete_invalid_admin(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_admin', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_booking_view(self):
        booking = Booking.objects.get(pk=11)
        response = self.client.post(reverse('delete_booking', args=[booking.id]))
        self.assertRedirects(response, reverse('manage_bookings'))
        self.assertFalse(Booking.objects.filter(pk=booking.id).exists())

    def test_delete_invalid_booking(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_booking', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_delete_lesson_view(self):
        lesson = Lesson.objects.get(pk=10)
        response = self.client.post(reverse('delete_lesson', args=[lesson.booking.id]))
        self.assertRedirects(response, reverse('manage_lessons'))
        self.assertFalse(Lesson.objects.filter(pk=lesson.booking_id).exists())
    
    def test_delete_invalid_lesson(self):
        invalid_id = 99999 #non-existent
        response=self.client.get(reverse('delete_lesson', args=[invalid_id]))
        self.assertEqual(response.status_code, 404)

    def test_manage_users_view_non_admin(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse('manage_users'))
        self.assertEqual(response.status_code, 403)

    def test_manage_students_view_non_admin(self):
        self.client.force_login(self.tutor)
        response = self.client.get(reverse('manage_students'))
        self.assertEqual(response.status_code, 403)
    
    def test_delete_self_admin_view(self):
        response = self.client.post(reverse('delete_user', args=[self.admin.id]))
        self.assertEqual(response.status_code, 403) 
        self.assertTrue(User.objects.filter(pk=self.admin.id).exists())

    def test_get_booking_view_as_admin(self):
        booking = Booking.objects.get(pk=11)
        response = self.client.get(reverse('get_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/booking.html')
        self.assertEqual(response.context['booking'], booking)

    def test_get_booking_view_as_student(self):
        self.client.force_login(self.student)
        booking = Booking.objects.get(student__user=self.student)
        response = self.client.get(reverse('get_booking', args=[booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/booking.html')
        self.assertEqual(response.context['booking'], booking)

    def test_get_lesson_view_as_admin(self):
        lesson = Lesson.objects.get(pk=10)
        response = self.client.get(reverse('get_lesson', args=[lesson.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/lesson.html')
        self.assertEqual(response.context['lesson'], lesson)

    def test_get_lesson_view_as_student(self):
        self.client.force_login(self.student)
        lesson = Lesson.objects.get(booking__student__user=self.student)
        response = self.client.get(reverse('get_lesson', args=[lesson.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/lesson.html')
        self.assertEqual(response.context['lesson'], lesson)

    def test_get_lesson_view_as_tutor(self):
        self.client.force_login(self.tutor)
        lesson = Lesson.objects.get(tutor__user=self.tutor)
        response = self.client.get(reverse('get_lesson', args=[lesson.booking.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entities/lesson.html')
        self.assertEqual(response.context['lesson'], lesson)
    
    def test_delete_tutor_as_admin(self):
        tutor_to_delete = Tutor.objects.get(user=self.tutor)
        response = self.client.post(reverse('delete_tutor', args=[self.tutor.id]))
        self.assertRedirects(response, reverse('manage_tutors'))
        self.assertFalse(Tutor.objects.filter(pk=tutor_to_delete.user.id).exists())  # Tutor should be deleted

    def test_delete_tutor_as_non_admin(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse('delete_tutor', args=[self.tutor.id]))
        self.assertEqual(response.status_code, 403) 
        self.assertTrue(Tutor.objects.filter(pk=self.tutor.id).exists())

    def test_delete_booking_as_admin(self):
        booking = Booking.objects.get(pk=11)
        response = self.client.post(reverse('delete_booking', args=[booking.id]))
        self.assertRedirects(response, reverse('manage_bookings'))
        self.assertFalse(Booking.objects.filter(pk=booking.id).exists())  # Booking should be deleted

    def test_delete_lesson_as_admin(self):
        lesson = Lesson.objects.get(pk=10)
        response = self.client.post(reverse('delete_lesson', args=[lesson.booking.id]))
        self.assertRedirects(response, reverse('manage_lessons'))
        self.assertFalse(Lesson.objects.filter(pk=lesson.booking.id).exists())