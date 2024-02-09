# forms.py
from django import forms
from .models import MelimitUser, MelimitStore
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
class MelimitStoreLoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'メールアドレスを入力してください'}))
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

# 全都道府県をリスト化(copilot依頼)
PREFECTURE_CHOICES = [('','選択してください'),('北海道','北海道'),('青森県','青森県'),('岩手県','岩手県'),('宮城県','宮城県'),('秋田県','秋田県'),('山形県','山形県'),('福島県','福島県'),('茨城県','茨城県'),('栃木県','栃木県'),('群馬県','群馬県'),('埼玉県','埼玉県'),('千葉県','千葉県'),('東京都','東京都'),('神奈川県','神奈川県'),('新潟県','新潟県'),('富山県','富山県'),('石川県','石川県'),('福井県','福井県'),('山梨県','山梨県'),('長野県','長野県'),('岐阜県','岐阜県'),('静岡県','静岡県'),('愛知県','愛知県'),('三重県','三重県'),('滋賀県','滋賀県'),('京都府','京都府'),('大阪府','大阪府'),('兵庫県','兵庫県'),('奈良県','奈良県'),('和歌山県','和歌山県'),('鳥取県','鳥取県'),('島根県','島根県'),('岡山県','岡山県'),('広島県','広島県'),('山口県','山口県'),('徳島県','徳島県'),('香川県','香川県'),('愛媛県','愛媛県'),('高知県','高知県'),('福岡県','福岡県'),('佐賀県','佐賀県'),('長崎県','長崎県'),('熊本県','熊本県'),('大分県','大分県'),('宮崎県','宮崎県'),('鹿児島県','鹿児島県'),('沖縄県','沖縄県')]
# MelimitStore用会員情報登録＆編集フォーム 
class MelimitStoreRegistrationForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    # password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitStore
        fields = ['email', 'password',  'username', 'postal_code', 'prefecture', 'city', 'address', 'phone_number', 'store_image', 'site_url']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'store-create-input-active',
                'placeholder': 'メールアドレスを入力してください（半角）',
                'required': True,
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
                'name': 'email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'store-create-input-active',
                'placeholder': 'パスワードを入力してください（半角英数字）',
                'required': True,
                'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,24}$',
                'name': 'password',
            }),
            # 'password_confirm': forms.PasswordInput(attrs={
            #     'class': 'store-create-input-active',
            #     'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,20}$',
            #     'placeholder': 'パスワードを再入力してください（半角）'
            # }),
            'username': forms.TextInput(attrs={
                'class': 'store-create-input-active',
                'pattern': '^.{1,20}$',
                'placeholder': '店舗名を入力してください',
                'name': 'username',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'store-create-input-active',
                'pattern': '^[0-9]{7}$',
                'placeholder': '郵便番号（半角数字）を入力してください（ハイフン不要）',
                'name': 'postal_code',
            }),
            'prefecture': forms.Select(choices=PREFECTURE_CHOICES, attrs={
                'class': 'store-create-input-active',
                'name': 'prefecture',
            }),
            'city': forms.TextInput(attrs={
                'class': 'store-create-input-active',
                'name': 'city',
            }),
            'address': forms.TextInput(attrs={
                'class': 'store-create-input-active',
                'name': 'address',
                }),
            'phone_number': forms.TextInput(attrs={
                'class': 'store-create-input-active',
                'pattern': '^[0-9]{10,11}$',
                'placeholder': '電話番号（半角数字）を市外局番から入力してください（ハイフン不要）',
                'name': 'phone_number',
            }),
            'store_image': forms.FileInput(attrs={
                'class': 'store-create-input-active',
                'name': 'store_image',
            }),
            'site_url': forms.URLInput(attrs={
                'class': 'store-create-input-active',
                'placeholder': 'WebサイトのURLがある場合は入力してください（半角）',
                'name': 'site_url',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_confirm'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'store-create-input-active',
                'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,20}$',
                'placeholder': 'パスワードを再入力してください（半角英数字）',
                'name': 'password_confirm',
            }),
            label='Confirm password'
        )
        if self.instance and self.instance.pk:
            # 編集のときはパスワードフィールドを削除
            self.fields.pop('password')
            self.fields.pop('password_confirm')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', 'パスワードが一致しません。')
        return cleaned_data
    
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


# ユーザー登録フォーム　'password_confirm'
class MelimitUserRegistrationForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput)
    # password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = MelimitUser
        fields = ['email', 'password', 'username', 'taste','postal_code', 'prefecture', 'city', 'address', 'phone_number']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'user-create-input-active',
                'placeholder': 'メールアドレスを入力してください（半角）',
                'required': True,
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
                'name': 'email',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'user-create-input-active',
                'placeholder': 'パスワードを入力してください（半角英数字）',
                'required': True,
                'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,24}$',
                'name': 'password',
            }),
            # 'password_confirm': forms.PasswordInput(attrs={
            #     'class': 'store-create-input-active',
            #     'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,20}$',
            #     'placeholder': 'パスワードを再入力してください（半角）'
            # }),
            'username': forms.TextInput(attrs={
                'class': 'user-create-input-active',
                'pattern': '^.{1,20}$',
                'placeholder': 'ユーザー名を入力してください',
                'name': 'username',
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'user-create-input-active',
                'pattern': '^[0-9]{7}$',
                'placeholder': '郵便番号（半角数字）を入力してください（ハイフン不要）'}),
                'prefecture': forms.Select(choices=PREFECTURE_CHOICES, attrs={
                'class': 'store-create-input-active',
                'name': 'postal_code',
            }),
            'city': forms.TextInput(attrs={
                'class': 'user-create-input-active',
                'name': 'city',
            }),
            'address': forms.TextInput(attrs={
                'class': 'user-create-input-active',
                'name': 'address',
                }),
            'phone_number': forms.TextInput(attrs={
                'class': 'user-create-input-active',
                'pattern': '^[0-9]{10,11}$',
                'placeholder': '電話番号（半角数字）を市外局番から入力してください（ハイフン不要）',
                'name': 'phone_number',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password_confirm'] = forms.CharField(
            widget=forms.PasswordInput(attrs={
                'class': 'user-create-input-active',
                'pattern': '^(?=.*?[a-z])(?=.*?\d)[a-z\d]{8,20}$',
                'placeholder': 'パスワードを再入力してください（半角英数字）',
                'name': 'password_confirm',
            }),
            label='Confirm password'
        )
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
            raise ValidationError("サーバーにそのメアドは登録されてないよ！")
        return email
