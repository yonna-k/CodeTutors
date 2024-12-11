from django.core.exceptions import ValidationError
from django.test import TestCase
from tutorials.models.student_model import Student
from tutorials.models.user_models import User
from django.contrib.auth.hashers import make_password

class StudentModelTestCase(TestCase):
    """Unit tests for the Student model."""

    def setUp(self):

        # Create a User instance
        user = User.objects.create_user(
            username='@teststudent',
            password=make_password('Password123'), #dodgy, should use seeder data instead
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
        )

        # Create the associated Student instance
        self.student = Student.objects.create(user=user, level='BEGINNER')


    def test_valid_student(self):
        self._assert_student_is_valid()

    def test_default_level_is_beginner(self):
        new_student = User.objects.create(
            username='@newstudent',
            password=make_password('Password123'),
            first_name='New',
            last_name='Student',
            email='newstudent@example.com'
        )

        self.nstudent = Student.objects.create(user=new_student)
        self.assertEqual(self.nstudent.level, 'BEGINNER')

    def test_level_can_be_beginner(self):
        self.student.level = 'BEGINNER'
        self._assert_student_is_valid()

    def test_level_can_be_intermediate(self):
        self.student.level = 'INTERMEDIATE'
        self._assert_student_is_valid()

    def test_level_can_be_advanced(self):
        self.student.level = 'ADVANCED'
        self._assert_student_is_valid()

    def test_level_cannot_be_invalid(self):
        self.student.level = 'EXPERT'
        self._assert_student_is_invalid()

    def test_level_cannot_be_blank(self):
        self.student.level = ''
        self._assert_student_is_invalid()


    # Helpers
    def _assert_student_is_valid(self):
        try:
            self.student.full_clean()
        except ValidationError:
            self.fail('Test student should be valid')

    def _assert_student_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.student.full_clean()
