from allauth.account.forms import SignupForm
from django import forms

class CustomSignupForm(SignupForm):
    is_typename = forms.BooleanField(required=False)