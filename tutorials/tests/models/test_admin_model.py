from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from tutorials.models.user_models import User
from tutorials.models.admin_model import Admin
from django.contrib.auth.hashers import make_password

class AdminModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@teststudent',
            password=make_password('Password123'),
            first_name='Test',
            last_name='Student',
            email='teststudent@example.com',
            role="admin"
        )

    def test_admin_creation_with_user(self):
        """Test that an Admin instance is created with a new user if none is provided."""
        initial_count = Admin.objects.count()
        admin = Admin(user=self.user)
        admin.save()
        self.assertEqual(admin.user.role, 'admin')  # Check the role
        self.assertEqual(Admin.objects.count(), initial_count + 1)

    def test_save_creates_user(self):
        admin = Admin()
        admin.save()
        user = User.objects.get(pk=admin.pk)
        self.assertEqual(user.role, 'admin')

        #assert that the Admin object is linked to the created User
        self.assertEqual(admin.user, user)

    def test_admin_str_method(self):
        """Test the string representation of the Admin model."""
        admin = Admin(user=self.user)
        admin.save()
        self.assertEqual(str(admin), self.user.get_full_name())

    
    

