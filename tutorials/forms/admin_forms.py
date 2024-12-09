from django import forms
from tutorials.models.lesson_models import Lesson
from tutorials.models.booking_models import Booking
from tutorials.models.user_models import User

class UpdateLessonForm(forms.ModelForm):
    "Form to edit a lesson"
    class Meta:
        model = Lesson
        fields = ['tutor']

class UpdateBookingForm(forms.ModelForm):
    "Form to edit a booking"
    class Meta:
        model = Booking
        fields = ['date', 'time', 'venue', 'frequency', 'duration', 'day', 'lang', 'status']

class UpdateUserForm(forms.ModelForm):
    "Form to edit a user"
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']