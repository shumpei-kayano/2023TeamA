# forms.py
from django import forms
from .models import MelimitUser, MelimitStore
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

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
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        # パスワードが入力されている場合(新規登録)はパスワードを設定
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


class MelimitUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitUser
        fields = ['email', 'password', 'password_confirm', 'username', 'postal_code', 'prefecture', 'city', 'address', 'phone_number']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

