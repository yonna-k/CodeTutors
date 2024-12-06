from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime, timedelta
from django.db import transaction
from tutorials.forms.booking_forms import BookingForm
from tutorials.models.booking_models import Booking
from tutorials.models.tutor_model import Tutor
from tutorials.models.lesson_models import Lesson
from tutorials.forms.lesson_forms import AssignTutorForm

def assign_tutor(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    #filter tutors based on the current booking's language and availability
    tutors = Tutor.objects.filter(
        #match language specialty
        **{f"specializes_in_{booking.lang.lower()}": True}, 
        #match day availability 
        **{f"available_{booking.day.lower()}": True}
    )

    if request.method == "POST":
        assign_form = AssignTutorForm(request.POST, tutors=tutors)
        booking_form = BookingForm(request.POST, instance=booking)

        #if booking details are changed
        if 'save_changes' in request.POST:
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.date = booking_form.cleaned_data['date']
                booking.save()
                messages.success(request, "Booking details updated successfully!")
                return redirect("assign_tutor", booking_id=booking.id)
            else:
                print("Form errors:", booking_form.errors)
        #if tutor is assigned
        elif 'assign_tutor' in request.POST: 
            if assign_form.is_valid():
                tutor = assign_form.cleaned_data['tutor']
                #check for conflicts with existing lessons
                if check_overlapping_lessons(tutor, booking):
                    messages.error(request, "This tutor is already booked for an overlapping lesson.")
                else:
                    #book lessons for the rest of the term
                    generate_recurring_lessons(booking, tutor)
                    #booking.delete()
                    messages.success(request, "Tutor assigned successfully and further lessons booked!")
                    return redirect("dashboard")
                
            if not assign_form.is_valid():
                print(f"Form errors: {assign_form.errors}")

    else:
        assign_form = AssignTutorForm(tutors=tutors)
        booking_form = BookingForm(instance=booking)

    return render(
        request,
        "assign_tutor.html",
        {
            "booking": booking,
            "assign_form": assign_form,
            "booking_form": booking_form,
            "no_tutors": not tutors.exists(),
        },
    )

#check if the tutor already has lessons that overlap with the current booking
def check_overlapping_lessons(tutor, booking):
    if not (tutor and booking.date and booking.time):
        raise ValueError("Tutor, date, or time is missing!")

    # Calculate the end time of the new booking
    minutes = 60 if booking.duration == "short" else 120
    start_time = booking.time
    end_time = (datetime.combine(booking.date, start_time) + timedelta(minutes=minutes)).time()

    #fetch all lessons for the same tutor and date
    lessons_on_date = Lesson.objects.filter(
        tutor=tutor,
        booking__date=booking.date
    )

    for lesson in lessons_on_date:
        #calculate the end time of each existing lesson
        lesson_start_time = lesson.booking.time
        lesson_end_time = (datetime.combine(lesson.booking.date, lesson_start_time) + timedelta(
            minutes=60 if lesson.booking.duration == "short" else 120
        )).time()

        #check for overlap
        if not (
            end_time <= lesson_start_time or  #current booking ends before or exactly when the existing lesson starts
            start_time >= lesson_end_time    #current booking starts after or exactly when the existing lesson ends
        ):
            return True  #overlap detected

    return False  #no overlap

#books lessons for the rest of the term for the student
def generate_recurring_lessons(booking, tutor):
    if not (booking.date and booking.time and booking.frequency):
        raise ValueError("Booking must have date, time, and frequency defined.")

    #calculate term dates and find the current term's end date
    booking_form = BookingForm()
    term_dates = booking_form.get_term_dates(booking.date.year)
    term_end_date = None
    for term_name, (term_start, term_end) in term_dates.items():
        if term_start <= booking.date <= term_end:
            term_end_date = term_end
            break
    if not term_end_date:
        raise ValueError("No valid term found for the booking date.")

    #determine the duration of the booking
    frequency = booking.frequency.lower()  #'weekly' or 'fortnightly'
    days_increment = 7 if frequency == "weekly" else 14

    #calculate recurring dates
    recurring_dates = []
    current_date = booking.date
    while current_date <= term_end_date:
        recurring_dates.append(current_date)
        current_date += timedelta(days=days_increment)

    #save lessons in the database
    with transaction.atomic():
        for lesson_date in recurring_dates:
            b = Booking.objects.create(
                student=booking.student,
                date=lesson_date,  #YYYY-MM-DD format
                time=booking.time,    #HH:MM:SS format
                frequency=booking.frequency,
                duration=booking.duration,
                day = booking.day,
                lang = booking.lang
            )
            l = Lesson.objects.create(
                booking=b,
                tutor=tutor,
            )
            #b.delete()
