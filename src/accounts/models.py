from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType # 追加
from django.contrib.auth.models import Permission # 追加
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
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        user = self._create_user(email, password, **extra_fields)

        # ユーザーにMelimitUserとMelimitStoreモデルの閲覧権限を付与
        # permission1 = Permission.objects.get(codename='view_melimituser')
        # permission2 = Permission.objects.get(codename='view_melimitstore')
        # user.user_permissions.add(permission1, permission2)

        # accountsアプリの全てのモデルの閲覧権限を取得
        content_types = ContentType.objects.filter(app_label='accounts')
        permissions = Permission.objects.filter(content_type__in=content_types, codename__startswith='view_')

        # ユーザーに全ての閲覧権限を付与
        for permission in permissions:
            user.user_permissions.add(permission)

        return user

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
    USER_TYPE_CHOICES = (
        ('melimit_user', 'MelimitUser'),
        ('melimit_store', 'MelimitStore'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True)
    # unique=Trueオプションを指定すると、メールアドレスフィールドは必須フィールドになる
    email = models.EmailField("メールアドレス", unique=True)
    # staffフィールドがTrueに設定されているユーザーは、Djangoの管理サイトにアクセスできる
    is_staff = models.BooleanField("is_staff", default=True)
    # 認証用のフィールド
    is_active = models.BooleanField("is_active", default=True)
    # 作成日時
    date_joined = models.DateTimeField("date_joined", default=timezone.now)
    # 名前
    username = models.CharField("名前（店舗名）", max_length=30, blank=True, unique=True)
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
        verbose_name_plural = "CustomUser"

class MelimitUser(CustomUser):
    def save(self, *args, **kwargs):
        self.user_type = 'melimit_user'
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "お客さん"
        verbose_name_plural = "MelimitUser"
        # login_redirect_url = '/home/'
    
    def __str__(self):
        return self.username
    
    



class MelimitStore(CustomUser):
    # 店舗画像
    store_image = models.ImageField(upload_to='store_image', blank=True)
    # サイトURL
    site_url = models.URLField("サイトURL", max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        self.user_type = 'melimit_store'
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "store"
        verbose_name_plural = "MelimitStore"
        # login_redirect_url = '/store/'
        
    
        def __str__(self):
            return 
    
        def __unicode__(self):
            return 
    
    def __str__(self):
        return self.username