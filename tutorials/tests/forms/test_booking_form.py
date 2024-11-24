from django import forms
from django.test import TestCase
from tutorials.forms.booking_forms import BookingForm


class BookingFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'date' : '2025-01-08',
            'time' : '14:00:00',
            'frequency' : 'weekly',
            'duration' : 'short'
        }

    def test_form_has_necessary_fields(self):
        form = BookingForm()
        self.assertIn('date', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('frequency', form.fields)
        self.assertIn('duration', form.fields)

    def test_valid_form(self):
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    
    #tests for date
    def test_date_must_be_in_future(self):
        self.form_input['date'] = '2023-03-01'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_must_be_in_current_or_next_year(self):
        self.form_input['date'] = '2030-02-09'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_must_not_be_in_current_term(self):
        self.form_input['date'] = '2024-12-18' #might become outdated
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_must_not_be_in_holiday(self):
        self.form_input['date'] = '2024-12-26' #might become outdated
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_date_must_be_on_weekday(self):
        self.form_input['date'] = '2025-02-22'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    #tests for time
    def test_date_must_be_after_nine(self):
        self.form_input['time'] = '08:00:00'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_date_can_be_nine(self):
        self.form_input['time'] = '09:00:00'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_date_must_be_before_five(self):
        self.form_input['time'] = '18:00:00'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_date_can_be_five(self):
        self.form_input['time'] = '17:00:00'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    #tests for frequency
    def test_frequency_can_be_fortnightly(self):
        self.form_input['frequency'] = 'fortnightly'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    #tests for duration
    def test_duration_can_be_long(self):
        self.form_input['duration'] = 'long'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
