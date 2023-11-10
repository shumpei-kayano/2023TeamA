# forms.py
from django import forms
from .models import MelimitUser, MelimitStore

class MelimitUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = MelimitUser
        fields = ('email', 'password', )  # 必要なフィールドを指定

class MelimitStoreRegistrationForm(forms.ModelForm):
    class Meta:
        model = MelimitStore
        fields = ('email', 'password', )  # 必要なフィールドを指定