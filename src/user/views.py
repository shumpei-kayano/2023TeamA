from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def index(request):
    print('Hello World!!!!')
    return render(request, 'user/index.html')
