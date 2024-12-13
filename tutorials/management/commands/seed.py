
from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError
from tutorials.models import Admin, User, Tutor, Student, Booking, Lesson
import pytz
from faker import Faker
from random import randint, choice, random, uniform
from datetime import datetime, timedelta, time

# Predefined users with roles (Admin/Tutor/Student)
user_fixtures = [
    {
        'username': '@johndoe',
        'email': 'john.doe@example.org',
        'first_name': 'John',
        'last_name': 'Doe',
        'role': 'admin',
    },
    {
        'username': '@janedoe',
        'email': 'jane.doe@example.org',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'role': 'tutor',
        'rate': 50.00,
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
        'role': 'student',
        'level': 'BEGINNER',
    }
]

booking_fixtures = [
    {
        'student_username': '@charlie',
        'date': '2023-12-15',
        'time': '10:00:00',
        'frequency': 'weekly',
        'duration': 'short',
        'day': 'Monday',
        'lang': 'Python',
    }
]

lesson_fixtures = [
    {
        'student_username': '@charlie',
        'tutor_username': '@janedoe',
    }
]


class Command(BaseCommand):
    USER_COUNT = 200
    TUTOR_COUNT = 15
    ADMIN_COUNT = 10
    STUDENT_COUNT = 100
    BOOKING_COUNT = 100
    LESSON_COUNT = 75
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'

    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_fixed_users()
        self.create_fixed_lessons()
        self.create_admins()
        self.create_tutors()
        self.create_students()
        self.create_bookings()
        self.create_lessons()
        print("Seeding complete.")

    def create_fixed_users(self):
        """Create predefined users from user_fixtures."""
        for data in user_fixtures:
            self.try_create_user(data)
    
    def create_admins(self):
        """Seed random Admin objects."""
        to_create = self.ADMIN_COUNT - Tutor.objects.count()
        for _ in range(to_create):
            self.generate_random_admin()

    def create_tutors(self):
        """Seed random Tutor objects."""
        to_create = self.TUTOR_COUNT - Tutor.objects.count()
        for _ in range(to_create):
            self.generate_random_tutor()
    
    def create_students(self):
        """Seed random Student objects."""
        to_create = self.STUDENT_COUNT - Student.objects.count()
        for _ in range(to_create):
            self.generate_random_student()

    def generate_random_admin(self):
        """Generate random students."""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)

        self.try_create_user({
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': 'admin',
        })

    def generate_random_student(self):
        """Generate random students."""
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        level = choice(['BEGINNER', 'INTERMEDIATE', 'ADVANCED'])

        self.try_create_user({
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': 'student',
            'level': level
        })
    
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
            'specializes_in_c': random() > 0.5,
            'specializes_in_ruby': random() > 0.5,
            'specializes_in_sql': random() > 0.5,
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
        
        self.try_create_user({
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'role': 'tutor',
            'rate': rate,
            **specialties,
            **availability
        })

    def try_create_user(self, data):
        """Try to create a user."""
        try:
            role = data.pop('role', 'other')
            profile_data = {k: v for k, v in data.items() if k not in ['username', 'email', 'password', 'first_name', 'last_name']}
            
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                password=self.DEFAULT_PASSWORD,
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=role
            )
            print(f"Created User #{user.id} ({user.username})")

            if role == 'tutor':
                Tutor.objects.create(user=user, **profile_data)
                print(f"Created Tutor profile for User #{user.id} ({user.username})")
            elif role == 'student':
                Student.objects.create(user=user, **profile_data)
                print(f"Created Student profile for User #{user.id} ({user.username})")
            elif role == 'admin':
                Admin.objects.create(user=user, **profile_data)
                print(f"Created Admin profile for User #{user.id} ({user.username})")
            else:
                raise ValueError(f"Invalid role for user: {data.get('username')}.")

        except IntegrityError as e:
            print(f"Error creating user {data.get('username')}: {e}")
            
    
    def create_bookings(self):
        """Create a specified number of random bookings for students."""
        student_count = Student.objects.count()

        if student_count == 0:
            print("Error: Not enough students to create bookings.")
            return

        for _ in range(self.BOOKING_COUNT):
            student = Student.objects.all()[randint(0, student_count - 1)]

            booking_date = datetime.now().date() + timedelta(days=randint(-30, 30))  # next/previous 30 days
            booking_time = time(randint(9, 17), choice([0, 30]))  # Random time between 9:00 to 17:00

            frequency = choice(['weekly', 'fortnightly'])
            duration = choice(['short', 'long'])
            day = choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
            lang = choice(['Python', 'Java', 'Ruby', 'C', 'SQL'])

            # Create the booking
            booking = Booking.objects.create(
                student=student,
                date=booking_date,
                time=booking_time,
                frequency=frequency,
                duration=duration,
                day=day,
                lang=lang,
            )

            print(f"Booking #{booking.id} created: Student #{student.user.id} ({student.user.username}) requests {day}, {booking_date} at {booking_time}, for {duration} lessons in {lang}.")

    def create_lessons(self):
        """Assign tutors to bookings and create lessons."""
        bookings = Booking.objects.filter(status='OPEN')  # Bookings without lessons
        tutor_count = Tutor.objects.count()

        if bookings.count() == 0 or tutor_count == 0:
            print("Error: No available bookings or tutors to create lessons.")
            return

        for i, booking in enumerate(bookings):
            if i >= self.LESSON_COUNT:
                break
            
            lang_field = f"specializes_in_{booking.lang.lower()}"
            day_field = f"available_{booking.day.lower()}"

            matching_tutors = Tutor.objects.filter(
                **{lang_field: True},  # Match language specialty
                **{day_field: True}   # Match day availability
            )
            if not matching_tutors.exists():
                print(f"No tutors available for Booking #{booking.id} ({booking.lang} on {booking.day}).")
                continue

            # Randomly select a tutor from the filtered queryset
            tutor = matching_tutors.order_by('?').first()

            booking.status = "CLOSED"
            booking.save()

            #tutor = Tutor.objects.all()[randint(0, tutor_count - 1)]
            Lesson.objects.create(
                booking=booking,
                tutor=tutor,
            )
            print(f"Lesson created for Booking #{booking.id} with Tutor #{tutor.user.id} ({tutor.user.username})")
    
    def create_fixed_bookings(self):
        """Create fixed bookings from students"""
        for booking_data in booking_fixtures:
            try:
                student = Student.objects.get(user__username=booking_data['student_username'])
                booking = Booking.objects.create(
                    student=student,
                    date=booking_data['date'],
                    time=booking_data['time'],
                    frequency=booking_data['frequency'],
                    duration=booking_data['duration'],
                    day=booking_data['day'],
                    lang=booking_data['lang']
                )
                print(f"Created fixed booking #{booking.id} for student {student.user.username} on {booking_data['date']} at {booking_data['time']}.")
            except Student.DoesNotExist:
                print(f"Student {booking_data['student_username']} does not exist.")
 
    def create_fixed_lessons(self):
        """Create fixed lessons from bookings and tutors"""
        for lesson_data in lesson_fixtures:
            try:
                student = Student.objects.get(user__username=lesson_data['student_username'])
                tutor = Tutor.objects.get(user__username=lesson_data['tutor_username'])
                booking = Booking.objects.filter(student=student).first()
                if booking:
                    Lesson.objects.create(booking=booking, tutor=tutor)
                    print(f"Created lesson for {tutor.user.username} with booking {booking.id} - {student.user.username} on {lesson_data['date']}.")
            except Student.DoesNotExist:
                print(f"Student {lesson_data['student_username']} does not exist.")
            except Tutor.DoesNotExist:
                print(f"Tutor {lesson_data['tutor_username']} does not exist.")


def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name.lower() + '.' + last_name.lower() + '@example.org'