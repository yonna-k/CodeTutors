from django.shortcuts import render

from tutorials.models import User

#TODO: use class like elsewhere in this file? e.g.: class AdminView():

#TODO: replace User filter with Student.objects.all(), Tutor.objects.all()...
def manage_students(request):
    "Renders the manage entities template with student data"
    students = User.objects.filter(first_name__startswith='s')
    return render(request, "manage_users.html", {'users': students})

def manage_tutors(request):
    "Renders the manage entities template with tutor data"
    tutors = User.objects.filter(first_name__startswith='t')
    return render(request, "manage_users.html", {'users': tutors})

def manage_bookings(request):
    "Renders the manage entities template with booking data"
    #TODO: fetch bookings from database and render 
    return False

#TODO: implement CRUD functionalities