from django import forms
from tutorials.models.lesson_model import Lesson
from tutorials.models.booking_model import Booking
from tutorials.models.user_models import User
<<<<<<< HEAD
from tutorials.models.admin_model import Admin

#TODO: Not implemented yet
=======

>>>>>>> d180e004bb72890fc15e755d513db3254ae770bd
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
<<<<<<< HEAD
        fields = ['username', 'first_name', 'last_name', 'email']

=======
        fields = ['username', 'first_name', 'last_name', 'email']
>>>>>>> d180e004bb72890fc15e755d513db3254ae770bd
