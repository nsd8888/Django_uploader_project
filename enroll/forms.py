from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Image,twitter_image

class ImageUpload(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['id','photo']
        labels = {'photo': ''}

class SignUpForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}

class face_form(forms.Form):
    face_access=forms.CharField(label='Enter the token Id',max_length=500)
    photo=forms.ImageField()
    message=forms.CharField(max_length=100)


class twitter_form(forms.ModelForm):
    class Meta:
        model=twitter_image
        fields='__all__'

class all_form(forms.Form):
    photo=forms.ImageField()
    message=forms.CharField(max_length=100)