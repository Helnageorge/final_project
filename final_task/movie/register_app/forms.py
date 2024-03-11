from django import forms
from .models import Registration



class EditProfileForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Registration
        fields = ['fname', 'lname', 'email','password']
