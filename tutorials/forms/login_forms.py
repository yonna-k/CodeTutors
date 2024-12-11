"""Forms for the tutorials app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from tutorials.models.user_models import User
from tutorials.models.tutor_model import Tutor
from tutorials.models.student_model import Student
from tutorials.models.admin_model import Admin

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
        level = self.cleaned_data.get('level')
        user.role = 'student'
        user.save()


        Student.objects.create(user=user, level=level)

        return user

class TutorSignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    LANGUAGES = ['Python', 'Java', 'C', 'Ruby', 'SQL']
    LANG_MAP = {
        "C" : "C", "SQL" : "SQL"
    }
    for lang in LANGUAGES:
        field_name = f'specializes_in_{LANG_MAP.get(lang, lang.lower())}'
        vars()[field_name] = forms.ChoiceField(
            choices=[('Yes', 'Yes'), ('No', 'No')],
            initial='No',
            widget=forms.Select,
            label=lang
        )

    # same for availability (like we did for languages)
    Days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for day in Days:
        field_name = f'available_{day.lower()}'
        vars()[field_name] = forms.ChoiceField(
            choices=[('Yes', 'Yes'), ('No', 'No')],
            initial='No',
            widget=forms.Select,
            label=day
        )

    # vars()['rate'] = forms.DecimalField(
    #     max_digits=5,
    #     decimal_places=2,
    #     initial=0.00,
    #     min_value=0,
    #     help_text="Enter your preferred hourly rate.",
    #     label="Hourly Rate"
    # )

    rate = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        max_value=999.99,
        min_value=0
    )


    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'specializes_in_python', 'specializes_in_java', 'specializes_in_C', 'specializes_in_ruby', 'specializes_in_SQL',
                  'available_monday', 'available_tuesday', 'available_wednesday', 'available_thursday', 'available_friday', 'available_saturday', 'available_sunday', 'rate']

    def save(self, commit=True):
        """Create a new user."""
        # Create the user object first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('new_password'))  # Set the password securely

        # Save the user object
        if commit:
            user.save()

        MAP = {
            "Yes" : True, "No" : False
        }

        # Set the role after the user is created
        role = self.cleaned_data.get('role')
        specializes_in_Python = MAP.get(self.cleaned_data.get('specializes_in_python'))
        specializes_in_Java = MAP.get(self.cleaned_data.get('specializes_in_java'))
        specializes_in_C = MAP.get(self.cleaned_data.get('specializes_in_C'))
        specializes_in_Ruby = MAP.get(self.cleaned_data.get('specializes_in_ruby'))
        specializes_in_SQL = MAP.get(self.cleaned_data.get('specializes_in_SQL'))
        available_Monday = MAP.get(self.cleaned_data.get('available_monday'))
        available_Tuesday = MAP.get(self.cleaned_data.get('available_tuesday'))
        available_Wednesday = MAP.get(self.cleaned_data.get('available_wednesday'))
        available_Thursday = MAP.get(self.cleaned_data.get('available_thursday'))
        available_Friday = MAP.get(self.cleaned_data.get('available_friday'))
        available_Saturday = MAP.get(self.cleaned_data.get('available_saturday'))
        available_Sunday = MAP.get(self.cleaned_data.get('available_sunday'))
        rate = self.cleaned_data.get('rate') 
        user.role = 'tutor'
        user.save()

        Tutor.objects.create(
            user=user, 
            specializes_in_python=specializes_in_Python, 
            specializes_in_java=specializes_in_Java, 
            specializes_in_C=specializes_in_C,
            specializes_in_ruby=specializes_in_Ruby,
            specializes_in_SQL=specializes_in_SQL,
            available_monday=available_Monday,
            available_tuesday=available_Tuesday,
            available_wednesday=available_Wednesday,
            available_thursday=available_Thursday,
            available_friday=available_Friday,
            available_saturday=available_Saturday,
            available_sunday=available_Sunday,
            rate=rate
        )


        return user

class AdminSignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up as admin."""
    
    
    class Meta:
        """Form options."""
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self, commit=True):
        """Create a new admin user."""
        # Create the user object first
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('new_password'))  # Set the password securely

        # Set the user as admin
        user.is_staff = True
        user.is_superuser = True

        # Save the user object
        if commit:
            user.save()

        # Set the role after the user is created
        user.role = 'admin'
        user.save()

        # Create an associated Admin object (if you have an Admin model)
        Admin.objects.create(user=user)

        return user
