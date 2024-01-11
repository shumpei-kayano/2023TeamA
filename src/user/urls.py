from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('explain/', views.explain_view, name='explain'),
    path('ana_ana/', views.anai, name='ana_ana'),
    path('omae_store_kokoha_useryou/', views.omae_store, name='omae_store'),
    path('omae_user_kokoha_storeyou/', views.omae_user, name='omae_user'),
    path('sinki/', views.sinki, name='sinki'),
    path('what-melimit/', views.what_melimit, name='what_melimit'),
    path('all-products/general/', views.all_products_general, name='all_products_general'),
    path('all-products/joint/', views.all_products_joint, name='all_products_joint'),
    path('contact/', views.contact, name='contact'),
    path('contact/confirm/', views.contact_confirm, name='contact_confirm'),
    path('contact/complete/', views.contact_complete, name='contact_complete'),
    path('all-products/general/general-products_detail/', views.general_products_detail, name='general_products_detail'),
    path('all-products/joint/joint-products_detail/', views.joint_products_detail, name='joint_products_detail'),
    path('cart/', views.cart, name='cart'),
]
