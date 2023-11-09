from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager # 追加
from django.contrib.auth.models import AbstractUser,PermissionsMixin,UserManager

# 複数種類のユーザーを管理するためのUserType
# class UserType(models.Model):
#     """ ユーザ種別 """
#     #typename = models.CharField(verbose_name='ユーザ種別',max_length=150)
#     is_typename = models.BooleanField("is_typename", default=False)
#     def __str__(self):
#         return f'{self.id} - {self.is_typename}'

# USERTYPE_DEFAULT = False


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
    # 顧客か店舗か判断するフィールド
    is_store = models.BooleanField("is_store", default=False)
    # モデルのオブジェクトを操作するためのマネージャーを定義 このモデルのCRUDができるマネージャー
    objects = UserManager()

    # USERNAME_FIELDはユーザーを一意に特定できるフィールドを指定する
    # 今回はemailにunique=Trueを指定している
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    #usertype = models.ForeignKey(UserType,verbose_name='ユーザ種別',null=True,on_delete=models.PROTECT)
    is_typename = models.BooleanField("is_typename", default=False)
    
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        db_table = 'custom_user'

    def __str__(self):
        return self.username

class MelimitUserDetail(models.Model):
    user = models.OneToOneField(CustomUser, unique=True, db_index=True, related_name='detail_MelimitUser', on_delete=models.CASCADE)
    # お客さん向けの項目(好み)
    
    class Meta:
        verbose_name = "お客さんの詳細"
        verbose_name_plural = "お客さんたちの詳細"

    def __str__(self):
        user = CustomUser.objects.get(pk=self.user_id)
        return f'{user.id} - {user.username} - {user.email} - {self.id}'

class MelimitStoreDetail(models.Model):
    user = models.OneToOneField(CustomUser, unique=True, db_index=True, related_name='detail_MelimitStore', on_delete=models.CASCADE)
    # 店舗向けの項目(商品)
    # # 商品名
    # product_name = models.CharField("商品名", max_length=30, blank=True)
    # # 商品画像
    # product_image = models.ImageField(upload_to='product_image', blank=True)
    # # 商品説明
    # product_description = models.TextField("商品説明", blank=True)
    # # 商品価格
    # product_price = models.IntegerField("商品価格", blank=True)
    # # 商品在庫数
    # product_stock = models.IntegerField("商品在庫数", blank=True)
    # # 商品カテゴリ
    # product_category = models.CharField("商品カテゴリ", max_length=30, blank=True)
    # # 商品タグ
    # product_tag = models.CharField("商品タグ", max_length=30, blank=True)
    # 店舗画像
    store_image = models.ImageField(upload_to='store_image', blank=True)
    # サイトURL
    site_url = models.URLField("サイトURL", max_length=200, blank=True)
    
    class Meta:
        verbose_name = "store"
        verbose_name_plural = "stores"
        
    def __str__(self):
        user = CustomUser.objects.get(pk=self.user_id)
        return f'{user.id} - {user.username} - {user.email} - {self.id}'