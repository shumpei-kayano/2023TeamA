from django.urls import path
from . import views
from .views import login_view

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
]
