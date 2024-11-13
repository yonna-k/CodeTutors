from django.db import models
from django.contrib.auth.models import User
#import student model

class Booking(models.Model):
    #add foreign key - student (requires student model)
    #student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="bookings")
    date = models.DateField()
    time = models.TimeField()
    VENUE_NAME = "Code Tutors HQ"
    venue = models.CharField(max_length=100, default=VENUE_NAME)

    FREQUENCY_CHOICES = [
        ("weekly", "weekly"),
        ("fortnightly", "fortnightly"),
    ]
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES) #, default="once a week"

    DURATION_CHOICES = [
        ("short", "short (1hr)"), #(database sees, user sees)
        ("long", "long (2hrs)"),
    ]
    duration = models.CharField(max_length=10, choices=DURATION_CHOICES) #, default="short"
    
    #timestamp - do we need this?
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #return f"Requested: Booking for {self.student} on {self.date} at {self.time}"
        return f"Requested: Booking on {self.date} at {self.time}"

