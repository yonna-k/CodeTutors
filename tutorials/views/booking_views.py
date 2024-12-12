from django.shortcuts import render, redirect
from tutorials.forms.booking_forms import BookingForm
from tutorials.models.student_model import Student
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# needs to be changed in accordance with the refactoring of Student model
@login_required
def create_booking(request):
    """View to handle booking creation."""
    if request.user.role != 'student':
        raise PermissionDenied
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                student = Student.objects.get(user=request.user)
                booking = form.save(commit=False)

                booking.student = student
                booking.date = form.cleaned_data['date']
                booking.save()
                messages.success(request, "Booking created successfully!")
                return redirect(f'{request.user.role}_dashboard')
            except Student.DoesNotExist:
                messages.error(request, "Only students can make a booking.")
                return redirect(f'{request.user.role}_dashboard')
        else:
            messages.error(request, "Invalid booking form. Please try again.")
    else:
        form = BookingForm()

    return render(request, 'book_session.html', {'form': form})
