from django import forms
from .models import Pet,AdoptionApplication
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import HiddenInput

class PetForm(UserCreationForm):
    class Meta:
        model = Pet
        fields = ['name', 'age', 'breed', 'description', 'photo']

class PetUpdateForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields= ['name', 'description']

class ImageUpdateForm(forms.ModelForm):

    class Meta:
        model= Pet
        fields = ['photo']

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class AdoptionApplicationForm(forms.ModelForm):
    class Meta:
        model = AdoptionApplication
        fields = ['pet_id', 'applicant_name', 'applicant_phone_number', 'applicant_email', 'vet_name', 'vet_phone_number', 'reason']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pet_id'].widget = HiddenInput()