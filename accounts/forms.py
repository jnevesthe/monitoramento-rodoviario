from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class Registrar(UserCreationForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name',  'password1', 'password2', 'foto']
        
class EditForm(UserChangeForm):
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'foto']        
