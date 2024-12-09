from django.db import models
from django.conf import settings
from .user_models import User

class Student(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    level = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='BEGINNER')

    def get_level(self):
        """Get the student's current level."""
        return self.level

    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'student_{self.pk}')
            user.role = 'student'
            user.level = self.level
            user.save()
            self.user = user
        super(Student, self).save(*args, **kwargs)
