from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from libgravatar import Gravatar
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


class User(AbstractUser):
    """Model used for user authentication, and team member related information."""

    Roles = (
        ('admin', 'Admin'),
        ('tutor', 'Tutor'),
        ('student', 'Student'),
    )

    username = models.CharField(
        max_length=30,
        unique=True,
        validators=[RegexValidator(
            regex=r'^@\w{3,}$',
            message='Username must consist of @ followed by at least three alphanumericals'
        )]
    )
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField(unique=True, blank=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(
        max_length=15,
        choices=Roles,
        default='student',
        blank=False
    )


    class Meta:
        """Model options."""

        ordering = ['last_name', 'first_name']

    def full_name(self):
        """Return a string containing the user's full name."""

        return f'{self.first_name} {self.last_name}'


    def gravatar(self, size=120):
        """Return a URL to the user's gravatar."""

        gravatar_object = Gravatar(self.email)
        gravatar_url = gravatar_object.get_image(size=size, default='mp')
        return gravatar_url

    def mini_gravatar(self):
        """Return a URL to a miniature version of the user's gravatar."""

        return self.gravatar(size=60)

class Tutor(models.Model):

    # id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tutor_profile'
    )

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

    # Hourly rate
    rate = models.DecimalField(
        max_digits=5,  # Maximum digits including decimal places
        decimal_places=2,  # Decimal places for currency
        validators=[MinValueValidator(0)],
        help_text="Enter your preferred hourly rate: "
    )

    def clean(self):
        super().clean()
        if self.rate < 0:
            raise ValidationError("Rate cannot be negative.")


    def get_specialties(self):

        specialties = [
            "Python" if self.specializes_in_python else None,
            "Java" if self.specializes_in_java else None,
            "C" if self.specializes_in_C else None,
            "Ruby" if self.specializes_in_ruby else None,
            "SQL" if self.specializes_in_SQL else None,
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

    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'tutor_{self.pk}')
            user.role = 'tutor'
            user.save()
            self.user = user
        super(Tutor, self).save(*args, **kwargs)

    def __str__(self):
        specialties = ', '.join(self.get_specialties()) or 'None'
        availability = 'Available' if any([self.available_monday, self.available_tuesday, self.available_wednesday, self.available_thursday, self.available_friday, self.available_saturday, self.available_sunday]) else 'Not Available'
        return f"{self.user.first_name} - {specialties} ({availability})"

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


    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'student_{self.pk}')
            user.role = 'student'
            user.save()
            self.user = user
        super(Student, self).save(*args, **kwargs)

class Admin(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='admin_profile'
    )
    # Add any admin-specific fields here

    def save(self, *args, **kwargs):
        if not self.user_id:
            user = User.objects.create(username=f'admin_{self.pk}')
            user.role = 'admin'
            user.save()
            self.user = user
        super(Admin, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.get_full_name()}'


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

class Lesson(models.Model):
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name="lesson"
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
