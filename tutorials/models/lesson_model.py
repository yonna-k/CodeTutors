from django.db import models
from .booking_model import Booking
from .tutor_model import Tutor

class Lesson(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="lesson",
        primary_key=True
    )
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE)


    #calculated dynamically
    @property
    def invoice(self):
        #maps duration to integer value
        DURATION_MULTIPLIER = {
            "short": 1,
            "long": 2,
        }
        multiplier = DURATION_MULTIPLIER.get(self.booking.duration, 1)
        if self.tutor.rate:
            return self.tutor.rate * multiplier
        return 0  #default to 0 if rate is missing

    def __str__(self):
        return f"Lesson on {self.booking.date} at {self.booking.time} with Tutor {self.tutor.user.first_name}, costing {self.invoice}"
