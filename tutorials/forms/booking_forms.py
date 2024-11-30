from datetime import date, timedelta, time
from dateutil import easter
from dateutil.relativedelta import relativedelta, MO, SU
from django import forms
from tutorials.models.booking_models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        #student field added after
        fields = ['day', 'time', 'frequency', 'duration', 'lang']

        time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

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
    
    def find_first_matching_date(self, term_dates, selected_day_number):
        # finds the first occurrence of the selected day in the given terms
        for term_name, (start_date, end_date) in term_dates.items():
            if start_date > date.today():
                #finds the first occurrence of the selected day in the term
                days_ahead = (selected_day_number - start_date.weekday() + 7) % 7
                first_matching_date = start_date + timedelta(days=days_ahead)

                #check if the matching date falls within the term
                if start_date <= first_matching_date <= end_date:
                    return first_matching_date

        #return None if no match is found
        return None
    
    def clean_day(self):
        selected_day = self.cleaned_data.get('day')
        term_dates = self.get_term_dates(date.today().year)

        if not selected_day:
            raise forms.ValidationError("Day is Required.")
        
        #maps each day to a value
        day_map = {
                'Monday': 0,
                'Tuesday': 1,
                'Wednesday': 2,
                'Thursday': 3,
                'Friday': 4,
                'Saturday': 5,
                'Sunday': 6,
            }
        
        if selected_day not in day_map:
            raise forms.ValidationError("Invalid day selected.")
        
        selected_day_number = day_map[selected_day]

        term_dates = self.get_term_dates(date.today().year)
        first_matching_date = self.find_first_matching_date(term_dates, selected_day_number)
        #if no match is found, calculate next year's terms and try again
        if not first_matching_date:
            next_year_term_dates = self.get_term_dates(date.today().year + 1)
            first_matching_date = self.find_first_matching_date(next_year_term_dates, selected_day_number)

        #if still no match, raise an error
        if not first_matching_date:
            raise forms.ValidationError("No matching day found in the upcoming terms.")

        #set the calculated date in the cleaned data
        self.cleaned_data['date'] = first_matching_date
        return selected_day  #return the validated day
                    

    