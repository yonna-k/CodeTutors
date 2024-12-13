from django.db import models
from .student_model import Student

class Booking(models.Model):
    # default 1 may cause issues if there is no Student
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="bookings", default=1)
    date = models.DateField()
    time = models.TimeField()
    VENUE_NAME = "Code Tutors HQ"
    venue = models.CharField(max_length=100, default=VENUE_NAME)

    # status of the booking
    STATUS = [
        ("OPEN", "OPEN"),
        ("CLOSED", "CLOSED")
    ]
    status = models.CharField(max_length=10, choices=STATUS, default="OPEN")

    # how often the Student would like their lessons
    FREQUENCY_CHOICES = [
        ("weekly", "weekly"),
        ("fortnightly", "fortnightly"),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default="weekly")

    DURATION_CHOICES = [
        ("short", "short (1hr)"), # (database sees, user sees)
        ("long", "long (2hrs)"),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES, default="short")

    # what day the student would like their lessons
    DAY_CHOICES = [
        ("Monday", "Monday"),
        ("Tuesday", "Tuesday"),
        ("Wednesday", "Wednesday"),
        ("Thursday", "Thursday"),
        ("Friday", "Friday")
    ]
    day = models.CharField(max_length=20, choices=DAY_CHOICES, default="Monday")

    # what programming language the student would like their lessons in
    PLANG_CHOICES = [
        ("Python", "Python"),
        ("Java", "Java"),
        ("Ruby", "Ruby"),
        ("C", "C"),
        ("SQL", "SQL")
    ]
    lang = models.CharField(max_length=20, choices=PLANG_CHOICES, default="Python")

    def __str__(self):
        return f"Requested: Booking for {self.student} on {self.date} at {self.time}"
