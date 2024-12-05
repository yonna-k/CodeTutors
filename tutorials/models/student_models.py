from . import User
from django.db import models

class Student(User):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    level = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='BEGINNER')

    def __str__(self):
        return f"{self.first_name} ({self.level})"