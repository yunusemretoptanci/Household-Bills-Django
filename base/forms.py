from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import Inovoice

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class InovoiceForm(ModelForm):
    class Meta:
        model = Inovoice
        fields = ('family','owner', 'description', 'price')
        
       