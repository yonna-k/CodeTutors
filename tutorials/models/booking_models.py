from django.db import models
from django.contrib.auth.models import User
from tutorials.models.student_models import Student
#import student model

class Booking(models.Model):
    # default 1 may cause issues if there is no Student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="bookings", default=1)
    date = models.DateField()
    time = models.TimeField()
    VENUE_NAME = "Code Tutors HQ"
    venue = models.CharField(max_length=100, default=VENUE_NAME)

    # how often the Student would like their lessons
    FREQUENCY_CHOICES = [
        ("weekly", "weekly"),
        ("fortnightly", "fortnightly"),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES) 

    DURATION_CHOICES = [
        ("short", "short (1hr)"), # (database sees, user sees)
        ("long", "long (2hrs)"),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES)
    

    def __str__(self):
        return f"Requested: Booking for {self.student} on {self.date} at {self.time}"

