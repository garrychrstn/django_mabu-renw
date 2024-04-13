from django import forms
from . models import *
from . choices import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from bootstrap_modal_forms.forms import BSModalModelForm

class NoteModelForm(BSModalModelForm):
    class Meta:
        model = Note
        exclude = ['profile', 'volume']
        


class UserProfile(forms.ModelForm):
    email = forms.EmailInput(
        # required=True,
    )
    first_name = forms.CharField(
        required=True,
    )
    last_name = forms.CharField(
        required=True
    )
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class SetProfile(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['account_created', 'username', 'books']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['note']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review', 'score']

class Register(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class SetProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['preference', 'blacklist']