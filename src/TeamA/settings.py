from pathlib import Path
import os
# debug_toolbarの設定
import mimetypes
mimetypes.add_type("application/javascript", ".js", True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9@wxshh*ph4og5afn_-r-uqjto5&^x16x&uk%pl(l0b(rg55+x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar', # 追加
    'sass_processor', # 追加
    'django_extensions', # 追加
    'django_cleanup', # 追加
    'user',
    'accounts',
    'django.contrib.sites', # 追加
    'allauth', # 追加
    'allauth.account', # 追加
    'allauth.socialaccount', # 追加
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware', # 追加
    'allauth.account.middleware.AccountMiddleware',  # 追加
]

INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost', '0.0.0.0'] # 追加

ROOT_URLCONF = 'TeamA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'accounts/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'TeamA.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'o-hara_db',
        'USER': 'admin',
        'PASSWORD': 'o-hara',
        'HOST': 'mysql_db', # dbのコンテナ名
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# 静的ファイルの設定
STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/nginx/html/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 画像ファイルのアップロード先の設定
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# debug_toolbarの設定
def show_debug_toolbar(request):
    return request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS

DEBUG_TOOLBAR_CALLBACK = show_debug_toolbar

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
    'STATIC_URL': '/debug_toolbar/',
}

# allauth用
SITE_ID = 1


# django-allauthの設定
# AUTHENTICATION_BACKENDSとは、認証バックエンドを指定する設定
# デフォルトでは、django.contrib.auth.backends.ModelBackendが指定されている
AUTHENTICATION_BACKENDS = (
    # ユーザー名とパスワードによる認証を行うバックエンド
    'django.contrib.auth.backends.ModelBackend',
    # Emailによる認証を行うバックエンドはAuthenticationBackendを使う
    'allauth.account.auth_backends.AuthenticationBackend',  # 追加
)

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'user:index'  # 追加
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'  # 追加

AUTH_USER_MODEL = 'accounts.CustomUser'  # 追加
# signupformからの情報をcustomusermodelに保存するためのアダプタを指定
ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'
