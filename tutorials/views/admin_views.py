from sqlite3 import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tutorials.models import User, Student, Tutor, Booking, Lesson, Admin
from tutorials.forms.login_forms import AdminSignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required


#TODO: use class based views?
#TODO: use login_required once Admin class made
#TODO: add pagination functionality

def is_admin(request):
    """Check if the user is an admin or the owner of the lesson"""
    if request.role == 'admin':
        return True
    raise PermissionDenied("You are not authorized to delete this lesson.")

@user_passes_test(is_admin)
def manage_users(request):
    """Renders the manage entities template with all user data"""
    users = User.objects.all().order_by('id')
    return render(request, "manage/manage_users.html", {'users': users})

@user_passes_test(is_admin)
def manage_students(request):
    """Renders the manage entities template with student data"""
    students = Student.objects.all().order_by('user__id')
    return render(request, "manage/manage_students.html", {'users': students})

@user_passes_test(is_admin)
def manage_tutors(request):
    """Renders the manage entities template with tutor data"""
    tutors = Tutor.objects.all().order_by('user__id')
    return render(request, "manage/manage_tutors.html", {'users': tutors})

@user_passes_test(is_admin)
def manage_admins(request):
    """Renders the manage entities template with admin data."""
    admins = Admin.objects.all().order_by('user__id')  # Replace Admin with your admin model
    return render(request, "manage/manage_admins.html", {'users': admins})

@user_passes_test(is_admin)
def manage_bookings(request):
    """Renders the manage entities template with booking data"""
    bookings = Booking.objects.filter(status="OPEN").order_by('id')
    return render(request, "manage/manage_bookings.html", {'bookings': bookings})

@user_passes_test(is_admin)
def manage_lessons(request):
    """Renders the manage entities template with lesson data"""
    lessons = Lesson.objects.all().order_by('booking_id')
    return render(request, "manage/manage_lessons.html", {'lessons': lessons})

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def get_user(request, id):
    "Renders the specific user template"
    user = get_object_or_404(User, pk=id)
    return render(request, 'entities/user.html', {'user': user})

@user_passes_test(is_admin)
def get_student(request, id):
    "Renders the specific student template"
    student = get_object_or_404(Student, user__id=id)
    return render(request, 'entities/student.html', {'student': student})

@user_passes_test(is_admin)
def get_tutor(request, id):
    "Renders the specific tutor template"
    tutor = get_object_or_404(Tutor, user__id=id)
    return render(request, 'entities/tutor.html', {'tutor': tutor})

@user_passes_test(is_admin)
def get_admin(request, id):
    "Renders the specific admin template."
    admin = get_object_or_404(Admin, user__id=id)
    return render(request, 'entities/admin-profile.html', {'admin': admin})

@login_required
def get_booking(request, id):
    "Renders the specific booking template"
    booking = get_object_or_404(Booking, pk=id)
    context = {'booking': booking, 'role': request.user.role}
    return render(request, 'entities/booking.html', context)

@login_required
def get_lesson(request, id):
    "Renders the specific lesson template"
    lesson = get_object_or_404(Lesson, booking__id=id)
    context = {'lesson': lesson, 'role': request.user.role}
    return render(request, 'entities/lesson.html', context)

@user_passes_test(is_admin)
def delete_user(request, id):
    "Delete the specified user"
    user = get_object_or_404(User, pk=id)
    user.delete()
    return redirect('manage_users')

@user_passes_test(is_admin)
def delete_student(request, id):
    "Delete the specified student as well as the user"
    student = get_object_or_404(Student, user__id=id)
    student.delete()
    return redirect('manage_students')

@user_passes_test(is_admin)
def delete_tutors(request, id):
    "Delete the specified tutor as well as the user"
    tutor = get_object_or_404(Tutor, user__id=id)
    tutor.delete()
    return redirect('manage_tutors')

@user_passes_test(is_admin)
def delete_admins(request, id):
    "Delete the specified admin as well as the associated user."
    admin = get_object_or_404(Admin, user__id=id)
    admin.delete()
    return redirect('manage_admins')

def delete_booking(request, id):
    "Delete the specified booking"
    booking = get_object_or_404(Booking, pk=id)
    if not(id == booking.id or request.user.role == "admin"):
        raise PermissionDenied("You are not authorized to delete this lesson.")
    booking.delete()
    if request.user.role == "admin":
        return redirect('manage_bookings')
    return redirect('dashboard')

def delete_lesson(request, id):
    "Delete the specific lesson as well as the booking"
    lesson = get_object_or_404(Lesson, booking_id=id)
    if not(id == lesson.booking.id or request.user.role == "admin"):
        raise PermissionDenied("You are not authorized to delete this lesson.")
    lesson.delete()
    if request.user.role == "admin":
        return redirect('manage_lessons')
    return redirect('dashboard')