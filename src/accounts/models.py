from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager # 追加

class UserManager(BaseUserManager):
    """カスタムユーザーマネージャー"""

    use_in_migrations = True

    # _はプライベートを表していて内部処理で実行される
    def _create_user(self, email, password, **extra_fields):
        # emailを必須にする
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        # emailを使ってUserデータを作成
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """カスタムユーザーモデル"""
    # unique=Trueオプションを指定すると、メールアドレスフィールドは必須フィールドになる
    email = models.EmailField("メールアドレス", unique=True)
    # staffフィールドがTrueに設定されているユーザーは、Djangoの管理サイトにアクセスできる
    is_staff = models.BooleanField("is_staff", default=False)
    # 認証用のフィールド
    is_active = models.BooleanField("is_active", default=True)
    # 作成日時
    date_joined = models.DateTimeField("date_joined", default=timezone.now)
    # 名前
    username = models.CharField("名前（店舗名）", max_length=30, blank=True)
    # 郵便番号
    postal_code = models.CharField("郵便番号", max_length=8, blank=True)
    # 都道府県
    prefecture = models.CharField("都道府県", max_length=10, blank=True)
    # 市区町村
    city = models.CharField("市区町村", max_length=50, blank=True)
    # 住所
    address = models.CharField("住所", max_length=100, blank=True)
    # 電話番号
    phone_number = models.CharField("電話番号", max_length=20, blank=True)
    
    # モデルのオブジェクトを操作するためのマネージャーを定義 このモデルのCRUDができるマネージャー
    objects = UserManager()

    # USERNAME_FIELDはユーザーを一意に特定できるフィールドを指定する
    # 今回はemailにunique=Trueを指定している
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []


    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

class MelimitUser(CustomUser):
    
    class Meta:
        verbose_name = "お客さん"
        verbose_name_plural = "お客さんたち"
        # login_redirect_url = '/home/'
    
    def __str__(self):
        return self.username
    
    



class MelimitStore(CustomUser):
    # 店舗画像
    store_image = models.ImageField(upload_to='store_image', blank=True)
    # サイトURL
    site_url = models.URLField("サイトURL", max_length=200, blank=True)
    
    class Meta:
        verbose_name = "store"
        verbose_name_plural = "stores"
        # login_redirect_url = '/store/'
        
    
        def __str__(self):
            return 
    
        def __unicode__(self):
            return 
    
    def __str__(self):
        return self.username