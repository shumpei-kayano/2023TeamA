# forms.py
from django import forms
from .models import MelimitUser, MelimitStore
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
class MelimitStoreLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MelimitStoreLoginForm, self).__init__(*args, **kwargs)
    class Meta:
        model = MelimitStore
        fields = ['email', 'password']
        
# class MelimitUserLoginForm(AuthenticationForm):
#     class Meta:
#         model = MelimitUser
#         fields = ['email', 'password']

# ModelFormだとmodelにpasswordフィールドが存在していないと使えない
# class MelimitUserLoginForm(forms.ModelForm):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop('request', None)
#         super().__init__(*args, **kwargs)
#     class Meta:
#         model = MelimitUser
#         fields = ('email', 'password', )  # 必要なフィールドを指定
        
# class MelimitUserLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput)
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
# class MelimitUserLoginForm(AuthenticationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
class MelimitUserLoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput)
 
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MelimitUserLoginForm, self).__init__(*args, **kwargs)
    class Meta:
        model = MelimitUser
        fields = ['email', 'password']

# MelimitStore用会員情報登録＆編集フォーム
class MelimitStoreRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitStore
        fields = ['email', 'password', 'password_confirm', 'username', 'postal_code', 'prefecture', 'city', 'address', 'phone_number', 'store_image', 'site_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # 編集のときはパスワードフィールドを削除
            self.fields.pop('password')
            self.fields.pop('password_confirm')

    def save(self, commit=True):
        # user = super().save(commit=False)
        # password = self.cleaned_data.get("password")
        # # パスワードが入力されている場合(新規登録)はパスワードを設定
        # if password:
        #     user.set_password(password)
        # if commit:
        #     user.save()
        # return user
        user = super().save(commit=True)  # commit=Trueに変更
        password = self.cleaned_data.get("password")
        # パスワードが入力されている場合(新規登録)はパスワードを設定
        if password:
            user.set_password(password)
            user.save()  # パスワードを設定した後に再度保存
        return user


# ユーザー登録フォーム
class MelimitUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitUser
        fields = ['email', 'password', 'password_confirm', 'username', 'taste','postal_code', 'prefecture', 'city', 'address', 'phone_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # 編集のときはパスワードフィールドを削除
            self.fields.pop('password')
            self.fields.pop('password_confirm')
    
    def save(self, commit=True):
        print('saveされているか確認！')
        print(f'self.cleaned_data: {self.cleaned_data}')
        user = super().save(commit=True)
        print(f'self.cleaned_data[taste]: {self.cleaned_data["taste"]}')
        # print(self.cleaned_data["taste"])
        user.taste = self.cleaned_data["taste"]
        print(f'user: {user}')
        # print(user)
        print(f'user.taste1: {user.taste}')
        # print(user.taste)
        password = self.cleaned_data.get("password")
        # パスワードが入力されている場合(新規登録)はパスワードを設定
        if password:
            user.set_password(password)
            print(f'user.taste2: {user.taste}')
            user.save()  # パスワードを設定した後に再度保存
        return user
            
    #パスワード１とパスワード２が違うときにform.is_validがfalseを返すようにするメソッド
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match")

        return cleaned_data

class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data['email']
        if not get_user_model().objects.filter(email=email).exists():
            print('サーバーにそのメアドないよ！')
            raise ValidationError("There is no user registered with the specified email address!")
        return email
