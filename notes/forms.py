
from django import forms
from django.contrib.auth.forms import UserCreationForm
from notes.models import *

class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ('title', 'description', 'order', 'is_done')

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'first_name', 'last_name',)