from django import forms
from django.test import TestCase
from tutorials.forms.booking_forms import BookingForm


class BookingFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'day' : 'Monday',
            'time' : '14:00:00',
            'frequency' : 'weekly',
            'duration' : 'short',
            'lang' : "Ruby"
        }

    def test_form_has_necessary_fields(self):
        form = BookingForm()
        self.assertIn('day', form.fields)
        self.assertIn('time', form.fields)
        self.assertIn('frequency', form.fields)
        self.assertIn('duration', form.fields)
        self.assertIn('lang', form.fields)

    def test_valid_form(self):
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())


    #tests for day
    def test_day_can_be_tuesday(self):
        self.form_input['day'] = "Tuesday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_day_can_be_wednesday(self):
        self.form_input['day'] = "Wednesday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_day_can_be_thursday(self):
        self.form_input['day'] = "Thursday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_day_can_be_friday(self):
        self.form_input['day'] = "Friday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_day_cannot_be_invalid(self):
        self.form_input['day'] = "Saturday"
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_day_cannot_be_blank(self):
        self.form_input['day'] = ""
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    #tests for date
    def test_date_is_on_monday(self):
        self.form_input['day'] = "Monday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        calculated_date = form.cleaned_data['date']
        self.assertEqual(calculated_date.weekday(), 0)
    
    def test_date_is_on_tuesday(self):
        self.form_input['day'] = "Tuesday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        calculated_date = form.cleaned_data['date']
        self.assertEqual(calculated_date.weekday(), 1)
    
    def test_date_is_on_wednesday(self):
        self.form_input['day'] = "Wednesday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        calculated_date = form.cleaned_data['date']
        self.assertEqual(calculated_date.weekday(), 2)

    def test_date_is_on_thursday(self):
        self.form_input['day'] = "Thursday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        calculated_date = form.cleaned_data['date']
        self.assertEqual(calculated_date.weekday(), 3)
    
    def test_date_is_on_friday(self):
        self.form_input['day'] = "Friday"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
        calculated_date = form.cleaned_data['date']
        self.assertEqual(calculated_date.weekday(), 4)


    #tests for time
    def test_time_must_be_after_nine(self):
        self.form_input['time'] = '08:00:00'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_time_can_be_nine(self):
        self.form_input['time'] = '09:00:00'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_time_must_be_before_five(self):
        self.form_input['time'] = '18:00:00'
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_time_can_be_five(self):
        self.form_input['time'] = '17:00:00'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_time_cannot_be_blank(self):
        self.form_input['time'] = ''
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    #tests for frequency
    def test_frequency_can_be_fortnightly(self):
        self.form_input['frequency'] = 'fortnightly'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_frequency_cannot_be_blank(self):
        self.form_input['frequency'] = ''
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    

    #tests for duration
    def test_duration_can_be_long(self):
        self.form_input['duration'] = 'long'
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_duration_cannot_be_blank(self):
        self.form_input['duration'] = ''
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())


    #tests for language
    def test_lang_can_be_java(self):
        self.form_input['lang'] = "Java"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_lang_can_be_ruby(self):
        self.form_input['lang'] = "Ruby"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())
    
    def test_lang_can_be_C(self):
        self.form_input['lang'] = "C"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_lang_can_be_SQL(self):
        self.form_input['lang'] = "SQL"
        form = BookingForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_lang_cannot_be_blank(self):
        self.form_input['lang'] = ""
        form = BookingForm(data=self.form_input)
        self.assertFalse(form.is_valid())