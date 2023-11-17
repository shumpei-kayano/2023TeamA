# forms.py
from django import forms
from .models import MelimitUser, MelimitStore
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class MelimitStoreLoginForm(AuthenticationForm):
    class Meta:
        model = MelimitStore
        fields = ['email', 'password']
class MelimitUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = MelimitUser
        fields = ('email', 'password', )  # 必要なフィールドを指定

class MelimitStoreRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitStore
        fields = ['email', 'password', 'password_confirm', 'username', 'postal_code', 'prefecture', 'city', 'address', 'phone_number', 'store_image', 'site_url']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
# 必要なフィールドを指定

# ユーザーが新規登録するフォーム
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    # user_type = forms.CharField(max_length=20,blank=True, null=True)
    # phone_number = forms.CharField(label="電話番号", max_length=20, blank=True)
    # postal_code = forms.CharField(label="郵便番号", max_length=8, blank=True)
    # prefecture = forms.CharField(label="都道府県", max_length=10, blank=True)
    # city = forms.CharField(label="市区町村", max_length=50, blank=True)
    # address = forms.CharField(label="丁目・番地・号", max_length=100, blank=True)
    

    class Meta:
        model = MelimitUser
        # fields = ("username", "email", "password1", "password2")
        fields = ("email", "password1", "password2","username","phone_number","postal_code","prefecture","city","address")
    # def clean_username(self):
    #     """Reject usernames that differ only in case."""
    #     username = self.cleaned_data.get("username")
    #     if (
    #         username
    #         and self._meta.model.objects.filter(username__iexact=username).exists()
    #     ):
    #         self._update_errors(
    #             ValidationError(
    #                 {
    #                     "username": self.instance.unique_error_message(
    #                         self._meta.model, ["username"]
    #                     )
    #                 }
    #             )
    #         )
    #     else:
    #         return username
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.user_type = 'melimit_user'
        if commit:
            user.save()
        return user
    
    # user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, blank=True, null=True)
    # # unique=Trueオプションを指定すると、メールアドレスフィールドは必須フィールドになる
    # email = models.EmailField("メールアドレス", unique=True)
    # # staffフィールドがTrueに設定されているユーザーは、Djangoの管理サイトにアクセスできる
    # is_staff = models.BooleanField("is_staff", default=True)
    # # 認証用のフィールド
    # is_active = models.BooleanField("is_active", default=True)
    # # 作成日時
    # date_joined = models.DateTimeField("date_joined", default=timezone.now)
    # # 名前
    # username = models.CharField("名前（店舗名）", max_length=30, blank=True)
    # # 郵便番号
    # postal_code = models.CharField("郵便番号", max_length=8, blank=True)
    # # 都道府県
    # prefecture = models.CharField("都道府県", max_length=10, blank=True)
    # # 市区町村
    # city = models.CharField("市区町村", max_length=50, blank=True)
    # # 住所
    # address = models.CharField("住所", max_length=100, blank=True)
    # # 電話番号
    # phone_number = models.CharField("電話番号", max_length=20, blank=True)
class MelimitUserEditForm(UserCreationForm):
    class Meta:
        model = MelimitUser
        fields = ('email',"password1", "password2", 'username', 'phone_number', 'postal_code', 'prefecture', 'city', 'address')
        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            user.user_type = 'melimit_user'
            if commit:
                user.save()
            return user