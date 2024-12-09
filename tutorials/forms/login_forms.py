"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from tutorials.models.user_models import User
from tutorials.models.tutor_model import Tutor
from tutorials.models.student_model import Student

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""

        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class StudentSignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""
    level = forms.ChoiceField(
        choices=[
            ('BEGINNER', 'Beginner'),
            ('INTERMEDIATE', 'Intermediate'),
            ('ADVANCED', 'Advanced')
        ],
        initial='BEGINNER',
        widget=forms.Select,  # Ensures it renders as a dropdown
        label='Level'
    )

    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'level']

    def save(self, commit=True):
        """Create a new user."""
        # Create the user object first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('new_password'))  # Set the password securely

        # Save the user object
        if commit:
            user.save()

        # Set the role after the user is created
        role = self.cleaned_data.get('role')
        user.role = 'student'
        user.save()


        Student.objects.create(user=user)

        return user

class TutorSignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    specializes_in_python = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        initial='No',
        widget=forms.Select,  # Ensures it renders as a dropdown
        label='Python'
    )
    specializes_in_java = forms.ChoiceField(
        choices=[
            ('Yes', 'Yes'),
            ('No', 'No'),
        ],
        initial='No',
        widget=forms.Select,  # Ensures it renders as a dropdown
        label='Java'
    )

    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'specializes_in_python', 'specializes_in_java', 'email']

    def save(self, commit=True):
        """Create a new user."""
        # Create the user object first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('new_password'))  # Set the password securely

        # Save the user object
        if commit:
            user.save()

        # Set the role after the user is created
        role = self.cleaned_data.get('role')
        user.role = 'tutor'
        user.save()

        Tutor.objects.create(user=user)


        return user
