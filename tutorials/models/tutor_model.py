from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Tutor(User):
    

    # Specialties - Example list of specialties as BooleanFields
    specializes_in_python = models.BooleanField(default=False)
    specializes_in_java = models.BooleanField(default=False)
    specializes_in_C = models.BooleanField(default=False)
    specializes_in_ruby = models.BooleanField(default=False)
    specializes_in_SQL = models.BooleanField(default=False)

    # Availability - Days of the week (True if available)
    available_monday = models.BooleanField(default=False)
    available_tuesday = models.BooleanField(default=False)
    available_wednesday = models.BooleanField(default=False)
    available_thursday = models.BooleanField(default=False)
    available_friday = models.BooleanField(default=False)
    available_saturday = models.BooleanField(default=False)
    available_sunday = models.BooleanField(default=False)

    # Hourly rate in the local currency
    rate = models.DecimalField(
        max_digits=3,  # Maximum digits including decimal places
        decimal_places=2,  # Decimal places for currency
        validators=[MinValueValidator(0)],
        help_text="Enter your preferred hourly rate: "
    )

    class Meta:
       
        ordering = ['rate', 'last_name']

    def get_specialties(self):
        
        specialties = [
            "Math" if self.specializes_in_math else None,
            "Science" if self.specializes_in_science else None,
            "English" if self.specializes_in_english else None,
            "Programming" if self.specializes_in_programming else None,
            "History" if self.specializes_in_history else None,
        ]
        return [specialty for specialty in specialties if specialty]

    def get_availability(self):

        availability = [
            "Monday" if self.available_monday else None,
            "Tuesday" if self.available_tuesday else None,
            "Wednesday" if self.available_wednesday else None,
            "Thursday" if self.available_thursday else None,
            "Friday" if self.available_friday else None,
            "Saturday" if self.available_saturday else None,
            "Sunday" if self.available_sunday else None,
        ]
        return [day for day in availability if day]

    def __str__(self):
        
        return f"{self.full_name()} - Rate: {self.rate}/hour"
