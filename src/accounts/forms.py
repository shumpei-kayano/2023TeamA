# forms.py
from django import forms
from .models import MelimitUser, MelimitStore

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