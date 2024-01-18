from django.urls import include,path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    # path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('create_root/', views.CreaterootView, name="create_root"),
    path('user_touroku/', views.UserCreateView, name='user_touroku'),
    path('store_touroku/', views.StoreCreateView, name='store_touroku'),
    # path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
    path('user_edit/',views.UserUpdateView.as_view(), name='user_edit'),
    # path('store_suceess/', views.StoreCreateSuccessView, name='store_success'),
    # path('store_edit/', views.StoreUpdateView.as_view(), name='store_edit'), # 店舗情報編集
    path('user_logout/', auth_views.LogoutView.as_view(next_page='user:index'), name='user_logout'),
    # path('touroku_success/',views.UserTourokuSuccess,name='touroku_success'),
    path('store_logout/', views.MelimitStoreLogoutView.as_view(), name='store_logout'),
    #パスワードリセット用
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    path('password_reset/', views.PasswordReset.as_view(), name='password_reset'), #追加
    path('password_reset/done/', views.PasswordResetDone.as_view(), name='password_reset_done'), #追加
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirm.as_view(), name='password_reset_confirm'), #追加
    path('reset/done/', views.PasswordResetComplete.as_view(), name='password_reset_complete'), #追加
    path('mypage/', views.MypageView, name='mypage'),
    path('touroku_confirm/', views.user_touroku_cfm, name='touroku_confirm'),
    path('touroku_success/', views.TourokuConfirm, name='touroku_success'),
]
