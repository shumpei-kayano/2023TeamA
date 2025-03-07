from pathlib import Path
from dotenv import load_dotenv
import os

from django.conf import settings  # 追加

# debug_toolbarの設定
import mimetypes
mimetypes.add_type("application/javascript", ".js", True)

# .envファイルを読み込む
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9@wxshh*ph4og5afn_-r-uqjto5&^x16x&uk%pl(l0b(rg55+x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['3.227.170.53', '107.20.9.122', 'teama.o-hara-oita.click', 'teama-sub.o-hara-oita.click']


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
    'store',
    'apscheduler', # 追加
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
    # 'allauth.account.middleware.AccountMiddleware',  # 追加
    'allauth.account.middleware.AccountMiddleware',  # 追加
]

INTERNAL_IPS = ['127.0.0.1', '::1', 'localhost', '0.0.0.0'] # 追加

ROOT_URLCONF = 'TeamA.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'user/templates', BASE_DIR / 'accounts/templates' ],
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
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASS'), # RDS作成時のパスワード
        # DB_HOSTにはRDSのエンドポイントを指定
        'HOST': os.getenv('DB_HOST'),  # envからHOSTを読み込む
        # 'HOST': 'teamaa-rds.czm4eswsq0yn.us-east-1.rds.amazonaws.com',  # 環境変数からHOSTを読み込む
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

# DB登録はUTCで行うが、テンプレート表示は日本時間にする
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
# authenticateメソッドで、backend引数を設定しない場合ここに設定しているバックエンドを順番に試し、
# 最初に成功したバックエンドを使う(成功後は次のバックエンドは試さない)
# つまり、all-authが使用されることはない？？
# ※backend引数を指定しても、全部動いてそう…なぜ…？
AUTHENTICATION_BACKENDS = (
    # MelimitUserModelBackendを使う
    'accounts.backends.MelimitUserModelBackend',  # 追加
    # MelimitStoreModelBackendを使う
    'accounts.backends.MelimitStoreModelBackend',  # 追加
    # ユーザー名とパスワードによる認証を行うバックエンド 
    'django.contrib.auth.backends.ModelBackend',
    # Emailによる認証を行うバックエンドはAuthenticationBackendを使う
    'allauth.account.auth_backends.AuthenticationBackend',  # 追加
)

# MelimitAccountAdapterを使う
ACCOUNT_ADAPTER = 'accounts.adapter.MelimitAccountAdapter'  # 追加

# ログイン/ログアウト後の遷移先を設定
# LOGIN_REDIRECT_URL = 'user:index'
# settings.LOGIN_REDIRECT_URL = settings.LOGIN_REDIRECT_URL.replace('#next', '')
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login_kkkk'  # 追加

AUTH_USER_MODEL = 'accounts.CustomUser'  # 追加

# ログインページのURLを設定(allauthのデフォルトを上書き)
# ここからログインすると、なぜかadapterを経由しない
# LOGIN_URL = 'account_login_kkkk'  # 追加

# ここからログインすると、adapterを経由して遷移する
# ユーザーが未ログイン状態でパスワードを変更すると遷移するページ
LOGIN_URL = 'account_login_kkkk'  # 追加

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# マイクロソフトのメールサービス、office365を使用する
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
# 使用しているoffice365のメールアドレスとパスワード
EMAIL_HOST_USER = 'ooi2272105@stu.o-hara.ac.jp'
EMAIL_HOST_PASSWORD = 'Pokemon6124m'
EMAIL_USE_TLS = True
# 開発用 コンソールに出力する
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# localhostからooi学番で送るとエラーが起こるので送信元をHOSTと同じにする
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SESSION_COOKIE_SECURE = True 
CSRF_COOKIE_SECURE = True

CSRF_TRUSTED_ORIGINS = [
    'https://*.o-hara-oita.click',
]
