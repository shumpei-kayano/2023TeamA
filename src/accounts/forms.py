from allauth.account.forms import LoginForm
from django import forms
from django.contrib.auth import authenticate


class CustomSignupForm(LoginForm):
    is_typename = forms.BooleanField(required=False)
    
    def save(self, request):
        self.user = super().save(request)
        return self.user
    
    def get_user(self):
        return self.user
    
class CustomLoginForm(LoginForm):
    is_typename = forms.BooleanField(required=False)
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        self.user_cache = authenticate(self.request, email=cleaned_data.get('email'), password=cleaned_data.get('password'))
        if self.user_cache is None:
            raise forms.ValidationError('Invalid username or password')
        return cleaned_data

    def get_user(self):
        return self.user_cache