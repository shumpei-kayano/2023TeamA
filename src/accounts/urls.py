from django.urls import include,path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('user_touroku/', views.UserCreateView.as_view(), name='user_touroku'),
    path('store_touroku/', views.StoreCreateView, name='store_touroku'),
    path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
    path('user_state_change/',views.edit_melimit_user,name='user_state_change'),
    # path('store_suceess/', views.StoreCreateSuccessView, name='store_success'),
    path('store_edit/', views.StoreUpdateView.as_view(), name='store_edit'),
    # path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
]
