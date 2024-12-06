from django import forms
from tutorials.models.tutor_model import Tutor

class AssignTutorForm(forms.Form):
    tutor = forms.ModelChoiceField(
        queryset=Tutor.objects.none(),
        label="Assign Tutor"
    )

    def __init__(self, *args, **kwargs):
        #dynamically set tutors if provided
        tutors = kwargs.pop('tutors', Tutor.objects.none())
        super().__init__(*args, **kwargs)
        self.fields['tutor'].queryset = tutors
        self.fields['tutor'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    def clean(self):
        cleaned_data = super().clean()
        tutor = cleaned_data.get("tutor")
        #ensure a tutor is selected
        if not tutor:
            raise forms.ValidationError("Please select a tutor.")
        return cleaned_data
