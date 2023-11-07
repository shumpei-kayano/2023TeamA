from django import forms
from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    # カスタムフィールドとバリデーションロジックをここに定義します
    # username = forms.CharField(max_length=254)
    # password = forms.CharField(widget=forms.PasswordInput)
    # store_image = forms.ImageField()
    pass