from django.shortcuts import render

from tutorials.models import User, Tutor, Booking

#TODO: use class based views?
#TODO: use @login_required once Admin class made

def manage_students(request):
    "Renders the manage entities template with student data"
    students = User.objects.all()
    return render(request, "manage_users.html", {'users': students, 'entity_name': "students"})

def manage_tutors(request):
    "Renders the manage entities template with tutor data"
    tutors = Tutor.objects.all()
    return render(request, "manage_users.html", {'users': tutors, 'entity_name': "tutors"})

def manage_bookings(request):
    "Renders the manage entities template with booking data"
    bookings = Booking.objects.all()
    return render(request, "manage_bookings.html", {'bookings': bookings, 'entity_name': "bookings"})

#TODO: implement CRUD functionalities