from django.db import models
from tutorials.models.booking_models import Booking
from tutorials.models.tutor_model import Tutor

class Lesson(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name="lesson")
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="lessons")

    def __str__(self):
        return f"Lesson on {self.booking.date} at {self.booking.time} with Tutor {self.tutor}"