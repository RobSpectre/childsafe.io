from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=255,
                                 required=False,
                                 help_text='Optional.')
    last_name = forms.CharField(max_length=255,
                                required=False,
                                help_text='Optional.')
    organization = forms.CharField(max_length=255,
                                   required=False,
                                   help_text='Optional.')
    email_address = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=30,
                                   required=False,
                                   help_text='Optional.')

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'organization',
                  'email_address',
                  'phone_number',
                  'password1',
                  'password2')
