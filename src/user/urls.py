from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('explain/', views.explain_view, name='explain'),
    path('ana_ana/', views.anai, name='ana_ana'),
    path('store_base/', views.store_base_view, name='store_base'),
    path('store_base_ikuyo/', views.store_base_ikuyo_view, name='store_base_ikuyo'),
    path('omae_store_kokoha_useryou/', views.omae_store, name='omae_store'),
    path('omae_user_kokoha_storeyou/', views.omae_user, name='omae_user'),
    path('sinki/', views.sinki, name='sinki'),
    path('what-melimit/', views.what_melimit, name='what_melimit'),
]
