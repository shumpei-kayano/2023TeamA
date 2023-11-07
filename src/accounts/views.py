from django.shortcuts import render

from allauth.account.views import LoginView
from .forms import CustomLoginForm

# Create your views here.

class StoreLoginView(LoginView):
    template_name = "account/anai.html"
<<<<<<< HEAD
    form_class = CustomLoginForm
    
    
    
=======
    form_class = CustomLoginForm
>>>>>>> 70588f18a93affe879ff87c1a5894095cf553430
