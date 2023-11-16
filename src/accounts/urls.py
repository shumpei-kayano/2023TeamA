from django.urls import include,path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('store_touroku/', views.StoreCreateView, name='store_touroku'),
]
