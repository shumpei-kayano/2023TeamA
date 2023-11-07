from django.shortcuts import render

from allauth.account.views import LoginView
from .forms import CustomLoginForm

# Create your views here.

class StoreLoginView(LoginView):
    template_name = "account/anai.html"
    form_class = CustomLoginForm
    
    
    