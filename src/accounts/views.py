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
from django.shortcuts import render
from django.urls import reverse
# Create your views here.
logger = logging.getLogger(__name__)

class CustomLoginView(LoginView):
    print('555')
    form_class = LoginForm
    def form_valid(self, form):
        print('あああああああああ')
        self.user = form.get_user()
        return super().form_valid(form)
    def get_success_url(self):
        if self.user.is_staff:
            return reverse('')
        else:
            return reverse('account/login')


class Store_login(LoginView):
    template_name = "account/store_login.html"
    # print('ううううううう')
    form_class = LoginForm
    
    def form_valid(self, form):
        print('あああああああああ')
        User = get_user_model()
        print('form_valid method was うわああああああああああ')
        
        pdb.set_trace()
        try:
            print('2222222222')
            user = User.objects.get(username=form.cleaned_data['login'])
            # user = User.objects.get(username=form.cleaned_data['username'])
            if not user.is_staff:
                print('333333')
                # return HttpResponseForbidden("えええええええええええええええええ!")
        except ObjectDoesNotExist:
            print('44444444')
            # return HttpResponseForbidden("いいいいいいいいいいいいい")
        return super().form_valid(form)
    # フォームのバリデーションが行われているか確認する
    def form_invalid(self, form):
        # pdb.set_trace()
        print('おおおおおおおおおおおおお')
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
