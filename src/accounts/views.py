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
from django.contrib.auth import authenticate, login
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
# def index(request):
#     return render(request, 'account/index.html')
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
    # def form_valid(self, form):
    #     print('MelimitUserLoginView')
    #     auth = authenticate(self.request,
    #                         username=form.cleaned_data['login'],
    #                         password=form.cleaned_data['password'],
    #                         backend='accounts.backends.MelimitUserModelBackend')
    #     if auth is not None:
    #         login(self.request, auth)
    #     return super().form_valid(form)
    # form_class = LoginForm
    # def form_valid(self, form):
    #     print('form_____')
    #     # フォームのデータを取得
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     print('form_valid_____')
    #     # authenticate関数にbackend引数を指定
    #     user = authenticate(self.request, username=username, password=password, backend='accounts.backends.MelimitStoreModelBackend')

    #     if user is not None:
    #         login(self.request, user)
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)
        
        
    def dispatch(self, request, *args, **kwargs):
        print('MelimitUserLoginView')
        # もしsessionにbackendが入っていたら、それを削除する
        if 'backend' in request.session:
            del request.session['backend']
        # sessionを出力してみる
        # print(f'session: {request.session}')
        # print(f'session: {dict(request.session)}')
        # ここで追加するセッションをもとにどのログインページからログインしようとしたか判断する(アダプターにて)
        request.session['backend'] = 'accounts.backends.MelimitUserModelBackend'
        print(f'session: {request.session}')
        print(f'session: {dict(request.session)}')
        print(request.session['backend'])
        return super().dispatch(request, *args, **kwargs)

class MelimitStoreLoginView(LoginView):
    template_name = 'account/store_login.html'  # MelimitStore用のカスタムテンプレート
    # def authenticate(self, *args, **kwargs):
    #     kwargs['backend'] = 'accounts.backends.MelimitStoreModelBackend'
    #     return super().authenticate(*args, **kwargs)
    # form_class = LoginForm
    # def form_valid(self, form):
    #     print('form_____')
    #     # フォームのデータを取得
    #     username = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     print('form_valid_____')
    #     # authenticate関数にbackend引数を指定
    #     user = authenticate(self.request, username=username, password=password, backend='accounts.backends.MelimitStoreModelBackend')

    #     if user is not None:
    #         login(self.request, user)
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)
        
    def dispatch(self, request, *args, **kwargs):
        print('MelimitStoreLoginView')
        if 'backend' in request.session:
            del request.session['backend']
        request.session['backend'] = 'accounts.backends.MelimitStoreModelBackend'
        print(f'session: {request.session}')
        print(f'session: {dict(request.session)}')
        return super().dispatch(request, *args, **kwargs)
    

# def UserCreateView(request):
#     return render(request, 'account/user_touroku.html')

def StoreCreateView(request):
    return render(request, 'account/store_touroku.html')

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/user_touroku.html'
    success_url = '/touroku/touroku_success/'
    
def UserTourokuSuccess(request):
    return render(request, 'account/user_after_touroku.html')