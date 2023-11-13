from django.shortcuts import render

# Create your views here.
def index(request):
    #return render(request, 'user/index.html')
    return render(request, 'index.html')

