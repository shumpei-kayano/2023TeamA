from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user.urls')),
    path('store/', include('store.urls')),
    path('accounts/store_login/', views.Store_login.as_view(), name='store_login'),  # 追加
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