from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from tutorials.models import User, Student, Tutor, Booking, Lesson, Admin
from tutorials.forms.login_forms import AdminSignUpForm
from django.http import Http404
from django.http import HttpResponse
from itertools import chain


#TODO: use class based views?
#TODO: use @login_required once Admin class made
#TODO: implement Create/Update functionalities
#TODO: add pagination functionality

def manage_users(request):
    "Renders the manage entities template with all user data"
    users = User.objects.all().order_by('id')
    return render(request, "manage/manage_users.html", {'users': users})

def manage_students(request):
    "Renders the manage entities template with student data"
    students = Student.objects.all().order_by('user__id')
    return render(request, "manage/manage_students.html", {'users': students})

def manage_tutors(request):
    "Renders the manage entities template with tutor data"
    tutors = Tutor.objects.all().order_by('user__id')
    return render(request, "manage/manage_tutors.html", {'users': tutors})

def manage_admins(request):
    "Renders the manage entities template with admin data."
    admins = Admin.objects.all().order_by('user__id')  # Replace Admin with your admin model
    return render(request, "manage/manage_admins.html", {'users': admins})


def manage_bookings(request):
    "Renders the manage entities template with booking data"
    bookings = Booking.objects.filter(status="OPEN").order_by('id')
    return render(request, "manage/manage_bookings.html", {'bookings': bookings})

def manage_lessons(request):
    "Renders the manage entities template with lesson data"
    lessons = Lesson.objects.all().order_by('booking_id')
    return render(request, "manage/manage_lessons.html", {'lessons': lessons})

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

def get_user(request, id):
    "Renders the specific user template"
    try:
        context = {'user': User.objects.get(pk=id)}
    except User.DoesNotExist:
        raise Http404(f"Could not find student with ID {id}")
    return render(request, 'entities/user.html', context)

def get_student(request, id):
    "Renders the specific student template"
    try:
        context = {'student': Student.objects.get(user__id=id)}
    except Student.DoesNotExist:
        raise Http404(f"Could not find student with ID {id}")
    return render(request, 'entities/student.html', context)

def get_tutor(request, id):
    "Renders the specific tutor template"
    try:
        context = {'tutor': Tutor.objects.get(user__id=id)}
    except Tutor.DoesNotExist:
        raise Http404(f"Could not find tutor with ID {id}")
    return render(request, 'entities/tutor.html', context)

def get_admin(request, id):
    "Renders the specific admin template."
    try:
        context = {'admin': Admin.objects.get(user__id=id)}  
    except Admin.DoesNotExist:
        raise Http404(f"Could not find admin with ID {id}")
    return render(request, 'entities/admin-profile.html', context)


def get_booking(request, id):
    "Renders the specific booking template"
    try:
        booking = Booking.objects.get(pk=id)
    except User.DoesNotExist:
        raise Http404(f"Could not find booking with ID {id}")
    context = {'booking': booking, 'role': request.user.role}
    return render(request, 'entities/booking.html', context)

def get_lesson(request, id):
    "Renders the specific lesson template"
    try:
        lesson = Lesson.objects.get(booking__id=id)
    except User.DoesNotExist:
        raise Http404(f"Could not find lesson with ID {id}")
    context = {'lesson': lesson, 'role' : request.user.role}
    return render(request, 'entities/lesson.html', context)

def delete_user(request, id):
    "Delete the specified user"
    try:
        user = User.objects.get(pk=id)
        user.delete()
    except User.DoesNotExist:
        raise Http404(f"Could not find user with ID {id}")
    return redirect('manage_users')

def delete_student(request, id):
    "Delete the specified student as well as the user"
    try:
        student = Student.objects.get(user__id=id)
        student.delete()
    except Student.DoesNotExist:
        raise Http404(f"Could not find student with ID {id}")
    return redirect('manage_students')

def delete_tutors(request, id):
    "Delete the specified tutor as well as the user"
    try:
        tutor = Tutor.objects.get(user__id=id)
        tutor.delete()
    except Tutor.DoesNotExist:
        raise Http404(f"Could not find tutor with ID {id}")
    return redirect('manage_tutors')

def delete_admins(request, id):
    "Delete the specified admin as well as the associated user."
    try:
        admin = Admin.objects.get(user__id=id)  # Replace Admin with your actual admin model
        admin.delete()
    except Admin.DoesNotExist:
        raise Http404(f"Could not find admin with ID {id}")
    return redirect('manage_admins')  # Replace with the name of your admin management URL


def delete_booking(request, id):
    "Delete the specified booking"
    try:
        booking = Booking.objects.get(pk=id)
        booking.delete()
    except Booking.DoesNotExist:
        raise Http404(f"Could not find booking with ID {id}")
    if request.user.role == "admin":
        return redirect('manage_bookings')
    return redirect('dashboard')

def delete_lesson(request, id):
    "Delete the specific lesson as well as the booking"
    try:
        lesson = Lesson.objects.get(booking_id=id)
        lesson.delete()
    except Lesson.DoesNotExist:
        raise Http404(f"Could not find lesson with ID {id}")
    if request.user.role == "admin":
        return redirect('manage_lessons')
    return redirect('dashboard')

