from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from allauth.account.views import LoginView
from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.urls import reverse
import logging
from django.urls import reverse_lazy

# Create your views here.

# class Store_login(LoginView):
#     template_name = "account/store_login.html"
#     form_class = LoginForm
    # def form_valid(self, form):
    #     # ユーザー名からユーザーを取得
    #     User = get_user_model()
    #     try:
    #         user = User.objects.get(username=form.cleaned_data['login'])
    #     except User.DoesNotExist:
    #         return super().form_valid(form)

    #     # is_staffのチェック
    #     if not user.is_staff:
    #         form.add_error(None, ValidationError("You are not authorized to log in."))
    #         return self.form_invalid(form)

    #     return super().form_valid(form)

class MelimitUserLoginView(LoginView):
    template_name = 'account/login.html'  # allauthのデフォルトテンプレート
    # def get_success_url(self):
    #     return reverse('user:ana_ana')  # ログイン成功後にリダイレクトするURL
    # def get_success_url(self):
    #     return reverse_lazy('user:ana_ana')  # ログイン後にリダイレクトするURL

class MelimitStoreLoginView(LoginView):
    template_name = 'account/store_login.html'  # MelimitStore用のカスタムテンプレート