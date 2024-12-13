from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tutorials.models import User, Student, Tutor, Booking, Lesson, Admin
from tutorials.forms.login_forms import AdminSignUpForm
from django.core.exceptions import PermissionDenied
from functools import wraps

def is_admin_required(view_func):
    """Decorator to check if the user is an admin."""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is an admin
        if not request.user.is_authenticated or request.user.role != 'admin':
            raise PermissionDenied("You are not authorized to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def check_admin_or_owner(user, instance):
    """Check if the user is an admin or the owner of the instance (Booking or Lesson)"""
    if user.role == "admin" or instance.user == user:
        return True
    raise PermissionDenied("You do not have permission to access this resource.")

@is_admin_required
def manage_users(request):
    """Renders the manage entities template with all user data"""
    users = User.objects.all().order_by('id')
    return render(request, "manage/manage_users.html", {'users': users})

@is_admin_required
def manage_students(request):
    """Renders the manage entities template with student data"""
    students = Student.objects.all().order_by('user__id')
    return render(request, "manage/manage_students.html", {'users': students})

@is_admin_required
def manage_tutors(request):
    """Renders the manage entities template with tutor data"""
    tutors = Tutor.objects.all().order_by('user__id')
    return render(request, "manage/manage_tutors.html", {'users': tutors})

@is_admin_required
def manage_admins(request):
    """Renders the manage entities template with admin data."""
    admins = Admin.objects.all().order_by('user__id')
    return render(request, "manage/manage_admins.html", {'users': admins})

@is_admin_required
def manage_bookings(request):
    """Renders the manage entities template with booking data"""
    bookings = Booking.objects.filter(status="OPEN").order_by('id')
    return render(request, "manage/manage_bookings.html", {'bookings': bookings})

@is_admin_required
def manage_lessons(request):
    """Renders the manage entities template with lesson data"""
    lessons = Lesson.objects.all().order_by('booking_id')
    return render(request, "manage/manage_lessons.html", {'lessons': lessons})

@is_admin_required
def add_admin(request):
    """Allow superusers to add new admin users."""
    if request.method == "POST":
        form = AdminSignUpForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new admin user
            return redirect("dashboard")
    else:
        form = AdminSignUpForm()

    return render(request, "add_admin.html", {"form": form})

@is_admin_required
def get_user(request, id):
    "Renders the specific user template"
    user = get_object_or_404(User, pk=id)
    return render(request, 'entities/user.html', {'user': user})

@is_admin_required
def get_student(request, id):
    "Renders the specific student template"
    student = get_object_or_404(Student, user__id=id)
    return render(request, 'entities/student.html', {'student': student})

@is_admin_required
def get_tutor(request, id):
    "Renders the specific tutor template"
    tutor = get_object_or_404(Tutor, user__id=id)
    return render(request, 'entities/tutor.html', {'tutor': tutor})

@is_admin_required
def get_admin(request, id):
    "Renders the specific admin template."
    admin = get_object_or_404(Admin, user__id=id)
    return render(request, 'entities/admin-profile.html', {'admin': admin})

def get_booking(request, id):
    "Renders the specific booking template"
    booking = get_object_or_404(Booking, pk=id)
    if request.user.role == "admin" or booking.student.user == request.user:
        context = {'booking': booking, 'role': request.user.role}
        return render(request, 'entities/booking.html', context)

    raise PermissionDenied("You do not have permission to view this booking.")

def get_lesson(request, id):
    "Renders the specific lesson template"
    lesson = get_object_or_404(Lesson, booking__id=id)
    booking = lesson.booking

    if request.user.role == "admin" or booking.student.user == request.user or lesson.tutor.user == request.user:
        context = {'lesson': lesson, 'role': request.user.role}
        return render(request, 'entities/lesson.html', context)

    raise PermissionDenied("You do not have permission to view this lesson.")

@is_admin_required
def delete_user(request, id):
    "Delete the specified user"
    user = get_object_or_404(User, pk=id)
    if user == request.user:
        raise PermissionDenied("You cannot delete yourself as an admin.")
    user.delete()
    return redirect('manage_users')

@is_admin_required
def delete_student(request, id):
    "Delete the specified student as well as the user"
    student = get_object_or_404(Student, user__id=id)
    student.delete()
    return redirect('manage_students')

@is_admin_required
def delete_tutors(request, id):
    "Delete the specified tutor as well as the user"
    tutor = get_object_or_404(Tutor, user__id=id)
    tutor.delete()
    return redirect('manage_tutors')

@is_admin_required
def delete_admins(request, id):
    "Delete the specified admin as well as the associated user."
    admin = get_object_or_404(Admin, user__id=id)
    if admin.user == request.user:
        raise PermissionDenied("You cannot delete yourself as an admin.")
    admin.delete()
    return redirect('manage_admins')

def delete_booking(request, id):
    "Delete the specified booking"
    booking = get_object_or_404(Booking, pk=id)
    if request.user.role == "admin" or booking.student.user == request.user:
        booking.delete()
        if request.user.role == "admin":
            return redirect('manage_bookings')
        return redirect('dashboard')
    
    raise PermissionDenied("You do not have permission to delete this booking.")

def delete_lesson(request, id):
    "Delete the specific lesson as well as the booking"
    lesson = get_object_or_404(Lesson, booking_id=id)
    booking = lesson.booking
    if request.user.role == "admin" or booking.student.user == request.user or lesson.tutor.user == request.user:
        booking.delete()
        if request.user.role == "admin":
            return redirect('manage_lessons')
        return redirect('dashboard')
    
    raise PermissionDenied("You do not have permission to delete this lesson.")
