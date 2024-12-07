from django.shortcuts import render, redirect

from tutorials.models import User, Student, Tutor, Booking, Lesson
from django.http import Http404

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
    students = Student.objects.all().order_by('id')
    return render(request, "manage/manage_students.html", {'users': students})

def manage_tutors(request):
    "Renders the manage entities template with tutor data"
    tutors = Tutor.objects.all().order_by('id')
    return render(request, "manage/manage_tutors.html", {'users': tutors})

def manage_bookings(request):
    "Renders the manage entities template with booking data"
    bookings = Booking.objects.all().order_by('id')
    return render(request, "manage/manage_bookings.html", {'bookings': bookings, 'entity_name': "booking"})

def manage_lessons(request):
    "Renders the manage entities template with lesson data"
    lessons = Lesson.objects.all().order_by('id')
    return render(request, "manage/manage_lessons.html", {'lessons': lessons, 'entity_name': "lesson"})

def get_user(request, id):
    "Renders the specific user template"
    try:
        context = {'user': User.objects.get(pk=id)}
    except User.DoesNotExist:
        raise Http404(f"Could not find student with ID {id}")
    return render(request, 'entities/user.html', context)

def get_student(request, id):
    "Renders the specific user template"
    try:
        context = {'user': Student.objects.get(pk=id)}
    except Student.DoesNotExist:
        raise Http404(f"Could not find student with ID {id}")
    return render(request, 'entities/student.html', context)

def get_tutor(request, id):
    "Renders the specific user template"
    try:
        context = {'user': Tutor.objects.get(pk=id)}
    except Tutor.DoesNotExist:
        raise Http404(f"Could not find tutor with ID {id}")
    return render(request, 'entities/tutor.html', context)

def get_booking(request, id):
    "Renders the specific booking template"
    try:
        context = {'booking': Booking.objects.get(pk=id)}
    except User.DoesNotExist:
        raise Http404(f"Could not find booking with ID {id}")
    return render(request, 'entities/booking.html', context)

def get_lesson(request, id):
    "Renders the specific lesson template"
    try:
        lesson = Lesson.objects.get(pk=id)
        context = {'lesson': lesson}
    except User.DoesNotExist:
        raise Http404(f"Could not find lesson with ID {id}")
    return render(request, 'entities/lesson.html', context)

def delete_user(request, id):
    try:
        user = User.objects.get(pk=id)
        user.delete()
    except User.DoesNotExist:
        raise Http404(f"Could not find user with ID {id}")
    return redirect('manage/manage_users')

def delete_booking(request, id):
    try:
        booking = Booking.objects.get(pk=id)
        booking.delete()
    except Booking.DoesNotExist:
        raise Http404(f"Could not find booking with ID {id}")
    return redirect('manage/manage_bookings')

def delete_lesson(request, id):
    try:
        lesson = Lesson.objects.get(pk=id)
        lesson.delete()
    except Lesson.DoesNotExist:
        raise Http404(f"Could not find lesson with ID {id}")
    return redirect('manage/manage_lessons')