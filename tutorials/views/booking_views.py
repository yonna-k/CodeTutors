from django.shortcuts import render, redirect
from tutorials.forms.booking_forms import BookingForm
from tutorials.models.student_models import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# needs to be changed in accordance with the refactoring of Student model
@login_required
def create_booking(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            try:
                #request.user of the type 'User'
                #need to get the Student object explicitly
                student = Student.objects.get(pk=request.user.pk)
                booking.student = student
                booking.date = form.cleaned_data['date']
                booking.save()
                return redirect('dashboard')
            except Student.DoesNotExist:
                #handle the case where the user is not a Student
                messages.error(request, "You must be a student to make a booking.")
                return redirect('dashboard')
    else:
        form = BookingForm()

    return render(request, 'book_session.html', {'form': form})
