from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('accounts/login/', views.MelimitUserLoginView.as_view(), name='account_login_kkkk'),
    # ここで指定したnameがallauth.urlsにあるnameと一致すると、そちらが優先される
    # 独自のviewを指定する場合は、allauthと被らないようにし、さらに、allauth.urlよりも上に書く必要がある
    path('accounts/store_login/', views.MelimitStoreLoginView.as_view(), name='store_login'),  # 追加
    # path('customer_login/',views.MelimitUserLoginView.as_view(),name='account_login_login'),
    path('touroku/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
]

# 画像のURLを追加
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# debug_toolbarの設定
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]