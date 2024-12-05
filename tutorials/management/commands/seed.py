from django.core.management.base import BaseCommand
from django.db import IntegrityError
from tutorials.models import User, Tutor, Student, Booking, Lesson
import pytz
from faker import Faker
from random import randint, choice, random, uniform
from datetime import datetime, timedelta, time

#TODO: Add admin model seeder!

# Predefined users with roles (Tutor/Student)
user_fixtures = [
    {
        'username': '@janedoe',
        'email': 'jane.doe@example.org',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'role': 'tutor',  # Specify the role
        'rate': 50.00,  # Tutor-specific field
        'specializes_in_python': True,
        'specializes_in_java': False,
        'available_monday': True,
        'available_tuesday': True,
        'available_wednesday': True,
    },
    {
        'username': '@charlie',
        'email': 'charlie.johnson@example.org',
        'first_name': 'Charlie',
        'last_name': 'Johnson',
        'role': 'student',  # Specify the role
        'level': 'BEGINNER',  # Student-specific field
    }
]

class Command(BaseCommand):
    USER_COUNT = 100
    TUTOR_COUNT = 30
    STUDENT_COUNT = 30
    BOOKING_COUNT = 30
    LESSON_COUNT = 20
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.create_tutors()
        self.create_students()
        self.create_bookings()
        self.create_fixed_lesson()
        self.create_lessons()
        print("Seeding complete.")

    def create_users(self):
        """Create predefined users from user_fixtures."""
        for data in user_fixtures:
            role = data.pop('role', 'user')
            if role == 'tutor':
                self.try_create_user(Tutor, data)
            elif role == 'student':
                self.try_create_user(Student, data)
            else:
                self.try_create_user(User, data)

    def create_tutors(self):
        """Seed random Tutor objects."""
        tutor_count = Tutor.objects.count()
        while tutor_count < self.TUTOR_COUNT:
            self.generate_random_tutor()
            tutor_count = Tutor.objects.count()

    def generate_random_tutor(self):
        """Generate random tutors."""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        rate = round(uniform(15, 100), 2)

        specialties = {
            'specializes_in_python': random() > 0.5,
            'specializes_in_java': random() > 0.5,
            'specializes_in_C': random() > 0.5,
            'specializes_in_ruby': random() > 0.5,
            'specializes_in_SQL': random() > 0.5,
        }
        availability = {
            'available_monday': random() > 0.5,
            'available_tuesday': random() > 0.5,
            'available_wednesday': random() > 0.5,
            'available_thursday': random() > 0.5,
            'available_friday': random() > 0.5,
            'available_saturday': random() > 0.5,
            'available_sunday': random() > 0.5,
        }

        self.try_create_user(Tutor, {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'rate': rate,
            **specialties,
            **availability
        })

    def create_students(self):
        """Seed random Student objects."""
        student_count = Student.objects.count()
        while student_count < self.STUDENT_COUNT:
            self.generate_random_student()
            student_count = Student.objects.count()

    def generate_random_student(self):
        """Generate random students."""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        level = choice(['BEGINNER', 'INTERMEDIATE', 'ADVANCED'])

        self.try_create_user(Student, {
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'level': level
        })

    

    def create_fixed_booking(self):
        """Create a booking for a predefined Student."""
        student = Student.objects.get(username='@charlie')
        booking_date = datetime.strptime("2024-12-31", "%Y-%m-%d").date()
        booking_time = datetime.strptime("12:00:00", "%H:%M:%S").time()
        frequency = 'weekly'
        duration = 'short'
        day = 'Monday'
        lang = 'Python'

        try:
            booking, created = Booking.objects.get_or_create(
                student=student,
                date=booking_date,
                time=booking_time,
                frequency=frequency,
                duration=duration,
                day=day,
                lang=lang,
            )
            if created:
                print(f"Fixed booking created: {student} requests {day}, {booking_date} at {booking_time}, for {duration} lessons in {lang}.")
            return booking

        except (Student.DoesNotExist) as e:
            print(f"Error creating fixed booking: {e}")
    
    def create_fixed_lesson(self):
        """Create a fixed lesson for @charlie with @janedoe using the fixed booking."""
        try:
            booking = self.create_fixed_booking()  # Get the fixed booking for @charlie
            tutor = Tutor.objects.get(username='@janedoe')

            lesson, created = Lesson.objects.get_or_create(
                booking=booking,
                tutor=tutor,
            )
            if created:
                print(f"Lesson created for [{booking}] with Tutor: {tutor}")
            return lesson
        
        except (Student.DoesNotExist, Tutor.DoesNotExist) as e:
            print(f"Error creating fixed lesson: {e}")
        
    
    def create_bookings(self):
        """Create a specified number of random bookings for students."""
        student_count = Student.objects.count()

        if student_count == 0:
            print("Error: Not enough students to create bookings.")
            return

        for _ in range(self.BOOKING_COUNT):
            student = Student.objects.all()[randint(0, student_count - 1)]

            booking_date = datetime.now().date() + timedelta(days=randint(1, 30))  # Next 30 days
            booking_time = time(randint(9, 17), choice([0, 30]))  # Random time between 9:00 to 17:00

            frequency = choice(['weekly', 'fortnightly'])
            duration = choice(['short', 'long'])
            day = choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            lang = choice(['Python', 'Java', 'Ruby', 'C', 'SQL'])

            # Create the booking
            Booking.objects.create(
                student=student,
                date=booking_date,
                time=booking_time,
                frequency=frequency,
                duration=duration,
                day=day,
                lang=lang,
            )

            print(f"Booking created: {student} requests {day}, {booking_date} at {booking_time}, for {duration} lessons in {lang}.")

    def create_lessons(self):
        """Assign tutors to bookings and create lessons."""
        bookings = Booking.objects.filter(lesson__isnull=True)  # Bookings without lessons
        tutor_count = Tutor.objects.count()

        if bookings.count() == 0 or tutor_count == 0:
            print("Error: No available bookings or tutors to create lessons.")
            return

        for i, booking in enumerate(bookings):
            if i >= self.LESSON_COUNT:
                break

            #TODO: Implement filtering for availability and specialties!

            tutor = Tutor.objects.all()[randint(0, tutor_count - 1)]
            Lesson.objects.create(
                booking=booking,
                tutor=tutor,
            )
            print(f"Lesson created for [{booking}] with Tutor: {tutor}")

    def try_create_user(self, model, data):
        """Try to create a user."""
        try:
            model.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=self.DEFAULT_PASSWORD,
                first_name=data['first_name'],
                last_name=data['last_name'],
                **{k: v for k, v in data.items() if k not in ['username', 'email', 'password', 'first_name', 'last_name']}
            )
        except IntegrityError as e:
            print(f"Error creating user: {e}")
        
        print(f"Creating {data['username']} as {model.__name__}") #TODO: Use a Booking ID?

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'