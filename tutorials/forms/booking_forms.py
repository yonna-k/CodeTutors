from datetime import date, timedelta, time
from dateutil import easter
from dateutil.relativedelta import relativedelta, MO, SU
from django import forms
from tutorials.models.booking_models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        #student field added after
        fields = ['date', 'time', 'frequency', 'duration']

        date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
        time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    def get_term_dates(self, year):
        #calculate Easter Sunday
        easter_date = easter.easter(year)

        #Term 1: First Monday in January to the Sunday before Easter
        first_monday_jan = date(year, 1, 1) + relativedelta(weekday=MO(+1))
        term_1_end = easter_date - timedelta(days=easter_date.weekday() + 1)  # Ensure it ends on a Sunday

        #Term 2: First Monday 2 weeks after Term 1 ends to the Sunday before July 18th (approximate end)
        term_2_start = term_1_end + timedelta(weeks=2)
        term_2_start = term_2_start + relativedelta(weekday=MO(+1))
        july_18 = date(year, 7, 18)
        term_2_end = july_18 + relativedelta(weekday=SU(-1))  # Ensure it ends on a Sunday

        #Term 3: First Monday in September to the Sunday 2 weeks before Term 1 (next year) starts
        first_monday_sep = date(year, 9, 1) + relativedelta(weekday=MO(+1))
        first_monday_jan_next = date(year+1, 1, 1) + relativedelta(weekday=MO(+1))
        term_3_end = first_monday_jan_next - timedelta(weeks=2)  # Two weeks before Term 1 starts
        term_3_end = term_3_end + relativedelta(weekday=SU(-1))  # Ensure it ends on a Sunday

        return {
            "Term 1": (first_monday_jan, term_1_end),
            "Term 2": (term_2_start, term_2_end),
            "Term 3": (first_monday_sep, term_3_end),
        }

    def clean_date(self):
        booking_date = self.cleaned_data.get('date')

        if not booking_date:
            raise forms.ValidationError("Date is required.")
        
        #check if date is not in the past/current date
        current_date = date.today()
        if booking_date <= current_date:
            raise forms.ValidationError("Bookings must be made in advance.")

        #check if the date is in the current/next year
        current_year = date.today().year
        if not (current_year <= booking_date.year <= current_year + 1):
            raise forms.ValidationError(f"Bookings must be within the current or next year.")
        
        #check if booking is not in current term (must be made before a term starts)
        term_dates = self.get_term_dates(booking_date.year)

        term_time = False
        for term, (start, end) in term_dates.items():
            if start <= booking_date <= end:
                term_time = True
                if start <= current_date <= end:
                    raise forms.ValidationError(f"Bookings should be made a term in advance. Current term: ({start} to {end}).")
        
        #check if booking is not in holiday period
        if not term_time:
            raise forms.ValidationError("Bookings should be made during term time, not holidays.")

        #check if the date is a Saturday or Sunday
        if booking_date.weekday() >= 5:  #5 = Saturday, 6 = Sunday
            raise forms.ValidationError("Bookings cannot be made on Saturdays or Sundays.")
        

        return booking_date


    def clean_time(self):
        booking_time = self.cleaned_data.get('time')

        if not booking_time:
            raise forms.ValidationError("Time is required.")
        
        start_time = time(9, 0)  # 9:00 AM
        end_time = time(17, 0)  # 5:00 PM

        # Check if the time is outside the valid range
        if not (start_time <= booking_time <= end_time):
            raise forms.ValidationError("Bookings can only be made between 9:00 AM and 5:00 PM.")

        return booking_time

    