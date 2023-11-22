from django.urls import include,path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'accounts'

urlpatterns = [
    # path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('store_touroku/', views.StoreCreateView, name='store_touroku'),
    # path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
    path('user_edit/',views.UserUpdateView.as_view(),name='user_edit'),
    # path('store_suceess/', views.StoreCreateSuccessView, name='store_success'),
    path('store_edit/', views.StoreUpdateView.as_view(), name='store_edit'),
    path('user_logout/', auth_views.LogoutView.as_view(next_page='user:index'), name='user_logout'),
    # path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
]
