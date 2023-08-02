from django import forms
from .models import Poll, Candidate

class AddPollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = [
            'title',
            'description',
        ]

        widgets={
            'title': forms.TextInput(
                attrs={
                'class': "form-control",
                'placeholder': "Enter poll name"
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': "form-control",
                    'placeholder': "Enter poll description"
                }
            )
        }

class CandidateForm(forms.ModelForm):
    gender_choice = (
        ("M", "Male"),
        ("F", "Female")
    )

    gender =  forms.ChoiceField(choices=gender_choice)
    class Meta:

        model = Candidate
        fields=[
            'name',
            'middle_name',
            'last_name',
            'age',
            'gender'
        ]

        widgets={
            'name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Enter candidate name"
                }
            ),
            'middle_name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Enter candidate middle name"
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Enter candidate last name"
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': "form-control",
                    'placeholder': "Enter candidate age"
                }
            ),

        }
