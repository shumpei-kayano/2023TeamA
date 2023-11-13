from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('ana_ana/', views.anai, name='ana_ana'),
    path('yoshi_yoshi/', views.yoshi, name='yoshi_yoshi'),
]
