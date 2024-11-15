from . import User
from django.db import models

class Student(User):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]

    level = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='BEGINNER'
)