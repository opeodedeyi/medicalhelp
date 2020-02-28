from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, MedicalInformation

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60)

    class Meta:
        model = CustomUser
        fields = ("email", "username", "medical_practitioner", "password1", "password2")


class AddMedForm(forms.ModelForm):

    class Meta:
        model = MedicalInformation
        fields = ["sickness", "duration", "location"]
