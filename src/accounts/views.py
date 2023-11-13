from django.shortcuts import render,redirect
from django.views import View
from django.http import HttpResponse
from allauth.account.views import LoginView
from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model,login
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
import logging
import pdb
# Create your views here.
logger = logging.getLogger(__name__)

class Store_login(LoginView):
    template_name = "account/store_login.html"
    # print('ううううううう')
    #form_class = LoginForm
    
    def form_valid(self, form):
        print('あああああああああ')
        # User = get_user_model()
        logger.info('form_valid method was うわああああああああああ')
        
        pdb.set_trace()
        try:
            user = form.user_cache
            # user = User.objects.get(username=form.cleaned_data['username'])
            if not user.is_typename:
                return HttpResponseForbidden("えええええええええええええええええ!")
        except ObjectDoesNotExist:
            return HttpResponseForbidden("いいいいいいいいいいいいい")
        return super().form_valid(form)
    # フォームのバリデーションが行われているか確認する
    def form_invalid(self, form):
        pdb.set_trace()
        logger.info('おおおおおおおおおおおおお')
        return super().form_invalid(form)
    
    
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
    
    

# class Customer_Login(LoginView):
#     template_name = "account/login.html"
