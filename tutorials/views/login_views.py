from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tutorials.forms.login_forms import LogInForm, PasswordForm, UserForm, StudentSignUpForm, TutorSignUpForm, AdminSignUpForm
from tutorials.helpers import login_prohibited
from tutorials.models import Booking, Lesson
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.http import Http404


@login_required
def dashboard(request):
    """Display the current user's dashboard."""

    if request.user.role == 'student':
        return redirect('student_dashboard')
    elif request.user.role == 'tutor':
        return redirect('tutor_dashboard')
    elif request.user.role == 'admin':
        return redirect('admin_dashboard')
    else:
        raise Http404("Invalid role.")

def forbidden(request):
    """Render the 403 page."""
    return render(request, '403.html')

def get_lessons(user, role):
    """Helper method to get previous and upcoming lessons."""
    now = timezone.now()
    if role == 'student':
        profile = user.student_profile
        filter_kwargs = {'booking__student': profile}
    elif role == 'tutor':
        profile = user.tutor_profile
        filter_kwargs = {'tutor': profile}
    else:
        raise PermissionDenied("Invalid role")

    previous_lessons = Lesson.objects.filter(
        **filter_kwargs,
        booking__date__lt=now.date()
    ) | Lesson.objects.filter(
        **filter_kwargs,
        booking__date=now.date(),
        booking__time__lt=now.time()
    )

    upcoming_lessons = Lesson.objects.filter(
        **filter_kwargs,
        booking__date__gt=now.date()
    ) | Lesson.objects.filter(
        **filter_kwargs,
        booking__date=now.date(),
        booking__time__gte=now.time()
    )
    
    return previous_lessons.distinct(), upcoming_lessons.distinct()

@login_required
def student_dashboard(request):
    """Display the student's dashboard."""
    if request.user.role != 'student':
        raise PermissionDenied

    student = request.user.student_profile
    bookings = Booking.objects.filter(student=student, status="OPEN")

    previous_lessons, upcoming_lessons = get_lessons(request.user, 'student')

    context = {
        'user': request.user,  # Corrected 'users' to 'user'
        'bookings': bookings,
        'previous_lessons': previous_lessons,
        'upcoming_lessons': upcoming_lessons,
    }
    return render(request, 'student_dashboard.html', context)

@login_required
def tutor_dashboard(request):
    """Display the tutor's dashboard."""
    if request.user.role != 'tutor':
        raise PermissionDenied
    
    previous_lessons, upcoming_lessons = get_lessons(request.user, 'tutor')

    context = {
        'users': request.user,
        'previous_lessons': previous_lessons,
        'upcoming_lessons': upcoming_lessons,
    }
    return render(request, 'tutor_dashboard.html', context)

@login_required
def admin_dashboard(request):
    """Render the admin's dashboard."""
    if request.user.role != 'admin':
        raise PermissionDenied
    return render(request, 'admin_dashboard.html', {'user': request.user})

def create_booking(request):
    if request.method == "POST":
        #TODO Handle booking form submission
        pass
    return render(request, 'create_booking.html')


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html')


class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""

        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            if (hasattr(user, "tutor_profile") or hasattr(user, "student_profile") or hasattr(user, "admin_profile")):
                login(request, user)
                return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

class TutorSignUpView(LoginProhibitedMixin, FormView):
    """Handle tutor sign-ups."""

    form_class = TutorSignUpForm
    template_name = "tutor_sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        """Save the tutor and set specialties."""
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
        
class StudentSignUpView(LoginProhibitedMixin, FormView):
    """Handle student sign-ups."""

    form_class = StudentSignUpForm
    template_name = "student_sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
class TutorSignUpView(LoginProhibitedMixin, FormView):
    """Handle tutor sign-ups."""

    form_class = TutorSignUpForm
    template_name = "tutor_sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        """Save the tutor and set specialties."""
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)

class AdminSignUpView(FormView):
    """Handle admin sign-ups."""
    
    form_class = AdminSignUpForm
    template_name = 'admin_sign_up.html'  # Template to render the admin sign-up form
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN  # Redirect URL if the user is logged in
    
    def form_valid(self, form):
        """Save the admin and log them in."""
        self.object = form.save()
        login(self.request, self.object)  # Automatically log the user in after creation
        return super().form_valid(form)
    
    def get_success_url(self):
        """Redirect to the configured URL after successful admin sign-up."""
        return reverse(self.redirect_when_logged_in_url)