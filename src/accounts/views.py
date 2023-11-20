from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
# from allauth.account.views import LoginView
# from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError
from django.urls import reverse
import logging
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import MelimitStoreRegistrationForm, MelimitStoreLoginForm, MelimitUserLoginForm, MelimitUserRegistrationForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MelimitStore, MelimitUser
# from .forms import MelimitStoreRegistrationForm, MelimitUserEditForm

from django.views.generic.edit import CreateView
# from .forms import CustomUserCreationForm, MelimitUserLoginForm
from django.contrib.auth.decorators import login_required
from .backends import MelimitUserModelBackend
from django.contrib.auth.views import LoginView


class MelimitUserLoginView(LoginView):
    template_name = 'account/login.html'  # MelimitStore用のカスタムテンプレート
    form_class = MelimitUserLoginForm
    
    def dispatch(self, request, *args, **kwargs):
        print('MelimitUserLoginView')
        if 'backend' in request.session:
            del request.session['backend']
        request.session['backend'] = 'accounts.backends.MelimitUserModelBackend'
        print(f'session: {request.session}')
        print(f'session: {dict(request.session)}')
        print(request.session['backend'])
        return super().dispatch(request, *args, **kwargs)
    # postリクエストが来るとログイン処理を行うview
    def post(self, request, *args, **kwargs):# selfを追加
        if request.method == 'POST':
            form = self.form_class(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                user = authenticate(request, email=email, password=password, backend='accounts.backends.MelimitUserModelBackend')
                if user is not None:
                    login(request, user)
                    print('login')
                    return render(request, 'user/index.html', {'form': form})
                else:
                    print('user is None 認証失敗')
                    form.add_error(None, 'メールアドレスまたはパスワードが間違っています。')  # ユーザーが認証できない場合のエラーメッセージ
            else:
                print(form.errors)
            print('ログイン失敗')
            return render(request, 'account/login.html', {'form': form})  # ログイン後のリダイレクト先を指定
            # else:
        #     # 認証に失敗した場合の処理を書く
        #     pass
        # if request.method == 'POST':
        #     form = MelimitUserRegistrationForm(request.POST)
        #     if form.is_valid():
        #         user = form.save()
        #         # backendを指定してログインさせる
        #         user.backend = 'accounts.backends.MelimitUserModelBackend'
                # login(request, user)
            # if user is not None:
        #     login(self.request, user)
        #     return super().form_valid(form)
        # else:
        #     return self.form_invalid(form)
    # def form_valid(self, form):
    #     # フォームのデータを取得
    #     email = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     # authenticate関数にbackend引数を指定
    #     user = authenticate(self.request, username=email, password=password, backend='accounts.backends.MelimitUserModelBackend')
    #     user = authenticate(username=email, password=password, backend='django.contrib.auth.backends.ModelBackend
    #     if user is not None:
    #         login(self.request, user)
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    
    

def UserCreateView(request):
    if request.method == 'POST':
        form = MelimitUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # backendを指定してログインさせる
            user.backend = 'accounts.backends.MelimitUserModelBackend'
            login(request, user)
            # return redirect('user:index')
            return render(request, 'user/index.html')
    else:
        form = MelimitUserRegistrationForm()
    return render(request, 'account/user_touroku.html', {'form': form})

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = MelimitUser
    form_class = MelimitUserRegistrationForm
    template_name = 'account/user_edit.html'
    success_url = reverse_lazy('user:index')

    def get_object(self, queryset=None):
        return self.request.user
    

class MelimitStoreLoginView(LoginView):
    template_name = 'account/store_login.html'  # MelimitStore用のカスタムテンプレート
    authentication_form = MelimitStoreLoginForm  # ここを追加
    
    # def form_valid(self, form):
    #     # フォームのデータを取得
    #     email = form.cleaned_data.get('username')
    #     password = form.cleaned_data.get('password')
    #     # authenticate関数にbackend引数を指定
    #     user = authenticate(self.request, username=email, password=password, backend='accounts.backends.MelimitStoreModelBackend')

    #     if user is not None:
    #         login(self.request, user)
    #         return super().form_valid(form)
    #     else:
    #         return self.form_invalid(form)
    # def dispatch(self, request, *args, **kwargs):
    #     print('MelimitStoreLoginView')
    #     if 'backend' in request.session:
    #         del request.session['backend']
    #     request.session['backend'] = 'accounts.backends.MelimitStoreModelBackend'
    #     print(f'session: {request.session}')
    #     print(f'session: {dict(request.session)}')
    #     return super().dispatch(request, *args, **kwargs)

def StoreCreateView(request):
    if request.method == 'POST':
        form = MelimitStoreRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # backendを指定してログインさせる
            user.backend = 'accounts.backends.MelimitStoreModelBackend'
            login(request, user)
            # return redirect('user:index')
            return render(request, 'user/index.html')
    else:
        form = MelimitStoreRegistrationForm()
    return render(request, 'account/store_touroku.html', {'form': form})

class StoreUpdateView(LoginRequiredMixin, UpdateView):
    model = MelimitStore
    form_class = MelimitStoreRegistrationForm
    template_name = 'account/store_edit.html'
    success_url = reverse_lazy('user:index')

    def get_object(self, queryset=None):
        return self.request.user
