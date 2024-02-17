from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
# from allauth.account.views import LoginView
# from allauth.account.forms import LoginForm
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.core.exceptions import ValidationError
from django.urls import reverse
import logging
from django.urls import reverse_lazy
from django.shortcuts import redirect
from .forms import MelimitStoreRegistrationForm, MelimitStoreLoginForm, MelimitUserLoginForm, MelimitUserRegistrationForm, CustomPasswordResetForm
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MelimitStore, MelimitUser
# from .forms import MelimitStoreRegistrationForm, MelimitUserEditForm

from django.views.generic.edit import CreateView
# from .forms import CustomUserCreationForm, MelimitUserLoginForm
from django.contrib.auth.decorators import login_required
from .backends import MelimitUserModelBackend
from django.contrib.auth.views import LoginView
from django.http import Http404
from accounts.mixins import MelimitModelMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
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
                    # ログイン後にuserのindexのビューを通るように変更
                    login(request, user)
                    print('login')
                    #return render(request, 'user/index.html', {'form': form})
                    # ログイン成功時にビューに遷移する
                    return redirect('user:index')
                #{% url 'user:index' %}
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
        print(f'きてるよ')
        # バリデーションをスキップし、直接セッションにデータを保存
        request.session['registration_data'] = request.POST
        return redirect('accounts:touroku_confirm')
    else:
        form = MelimitUserRegistrationForm()
    return render(request, 'account/user_touroku.html', {'form': form})
    # if request.method == 'POST':
    #     form = MelimitUserRegistrationForm(request.POST)
    #     print(f'きてるよ')
    #     if form.is_valid():
    #         user = form.save(commit=False)
    #         # backendを指定してログインさせる
    #         # user.backend = 'accounts.backends.MelimitUserModelBackend'
    #         # login(request, user)
    #         # return redirect('user:index')
    #         request.session['registration_data'] = request.POST
    #         return redirect('accounts:touroku_confirm')
    #     else:
    #         print(form.errors)
    # else:
    #     form = MelimitUserRegistrationForm()
    # return render(request, 'account/user_touroku.html', {'form': form})


# class UserUpdateView(LoginRequiredMixin, UpdateView):
#     model = MelimitUser
#     form_class = MelimitUserRegistrationForm
#     # form_class = MelimitUserUpdateForm
#     template_name = 'account/user_edit.html'
#     success_url = reverse_lazy('user:index')

#     def get_object(self, queryset=None):
#         print(f'aaaaa :{self.request.session.get("user_id")}')
#         # print(f'session: {request.session}')
#         print(f'self: {self}')
#         user_id = self.request.user.id
#         # user_id = self.request.session.get('user_id')
#         print(f'user_id: {user_id}')
#         user = MelimitUser.objects.get(id=user_id)
#         print('zzzzzzzzzzzzzzz')
#         return user
    
class UserUpdateView(LoginRequiredMixin, UpdateView, MelimitModelMixin):
    model = MelimitUser
    form_class = MelimitUserRegistrationForm
    template_name = 'account/user_edit.html'
    success_url = reverse_lazy('accounts:mypage')

    def get_object(self, queryset=None):
        user = self.get_melimitmodel_user()
        print(f'user.__class__.__name__: {user.__class__.__name__}')
        # isinstanceでuserがMelimitUserのインスタンスかどうかを判定
        print(isinstance(user, MelimitUser))
        return user
    
    
# MelimitStore用のログイン画面への遷移
class MelimitStoreLoginScreenView(LoginView):
    template_name = 'account/store_login.html'  # MelimitStore用のカスタムテンプレート
    authentication_form = MelimitStoreLoginForm  # ここを追加

# MelimitStore用のログアウト処理(クラスベースビュー)
class MelimitStoreLogoutView(View):
    def get(self, request, *args, **kwargs):
        # ログアウト処理
        logout(request)
        return redirect('store_login')

# MelimitStore用の新規登録
def StoreCreateView(request):
    if request.method == 'POST':
        print('店舗登録post')
        form = MelimitStoreRegistrationForm(request.POST)
        if form.is_valid():
            request.user = form.save()
            print(f'request.user: {request.user.__dict__}')
            print(f'request: {request.__dict__}')
            # backendを指定してログインさせる
            request.user.backend = 'accounts.backends.MelimitStoreModelBackend'
            # user.user_type = 'melimit_store'
            mixin = MelimitModelMixin()
            mixin.request = request
            # print(f'user: {user.__dict__}')
            user = mixin.get_melimitmodel_user()
            # model_name = type(user).__name__
            # instance_name = type(user).__name__
            # セッションにモデル名とインスタンス名を保存
            # request.session['model_name'] = model_name
            # request.session['instance_name'] = instance_name
            login(request, request.user)
            # セッション'model_name'と'instance_name'を出力してみる
            # print(f'model_name: {request.session["model_name"]}')
            # print(f'instance_name: {request.session["instance_name"]}')
            # return render(request, 'store/base.html', {
            #     'model_name': request.session['model_name'],
            #     'instance_name': request.session['instance_name']
            # })
            return redirect('store:index')
        else:
            print('店舗登録失敗')
            print(f'失敗フォームエラー: {form.errors}')
            return render(request, 'store/store-create.html', {'form': form})
    # POSTでない場合は空のフォームを生成(最初のページ表示時)
    else:
        form = MelimitStoreRegistrationForm()
    return render(request, 'store/store-create.html', {'form': form})

# MelimitStore用の会員情報編集
class StoreUpdateView(LoginRequiredMixin, UpdateView, MelimitModelMixin):
    model = MelimitStore
    form_class = MelimitStoreRegistrationForm
    template_name = 'account/store_edit.html'
    success_url = reverse_lazy('user:store_base')

    def get_object(self, queryset=None):
        user = self.get_melimitmodel_user()
        # セッション情報取得
        # model_name = self.request.session.get('model_name')
        # instance_name = self.request.session.get('instance_name')
        # print(f'model: {model_name}')
        # print(f'instance: {instance_name}')
        # idからユーザー情報を取得
        # store_id = self.request.session.get('store_id')
        # print(f'store_id: {store_id}')
        # user = MelimitStore.objects.get(id=store_id)
        # userのインスタンス名は'user = self.request.user'で取得した場合は'CustomUser'になる
        # idがらオブジェクトを取得した場合は'MelimitStore'になる
        print(f'user.__class__.__name__: {user.__class__.__name__}')
        # isinstanceでuserがMelimitStoreのインスタンスかどうかを判定
        print(isinstance(user, MelimitStore))
        # if isinstance(user, MelimitStore):
        #     return user
        # else:
        #     raise Http404("User is not a MelimitStore instance")
        return user
    # なくても処理できる？？？
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     # 編集時には既存のオブジェクトをフォームにセットする
    #     kwargs['instance'] = self.get_object()
    #     return kwargs
    
# パスワードリセット用のビュー達
class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    """パスワード変更ビュー"""
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'account/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'account/password_change_done.html'


# --- ここから追加
class PasswordReset(PasswordResetView):
    form_class = CustomPasswordResetForm
    # オーバーライドもとに email_template_name = "registration/password_reset_email.html"があり、変える必要あり
    # どんな内容のメールを送るのかの設定
    """パスワード変更用URLの送付ページ"""
    # subject_template_name = 'accounts/mail_template/reset/subject.txt'
    # email_template_name = 'accounts/mail_template/reset/message.txt'
    
    #メアドがデータベースに存在するか確認必須！！！！！！！！
    
    email_template_name = 'account/password_email.html'

    template_name = 'account/password_reset_form.html'
    success_url = reverse_lazy('accounts:password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'account/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    success_url = reverse_lazy('accounts:password_reset_complete')
    template_name = 'account/password_reset_confirm.html'
    print('パスワード設定するビュー')
    def form_valid(self, form):
        response = super().form_valid(form)
        print("Form has been submitted successfully")
        return response

class PasswordResetComplete(PasswordResetCompleteView):
    print('パスワード再設定後のビュー')
    """新パスワード設定しましたページ"""
    template_name = 'account/password_reset_complete.html'
    
# class CreaterootView(View):
#     template_name = 'account/create_root.html'
def CreaterootView(request):
    return render(request, 'account/create_root.html')

# マイページへの遷移
def MypageView(request):
    return render(request, 'account/mypage.html')


def user_touroku_cfm(request):
    print('cfmcfm')
    if 'registration_data' in request.session:
        form = MelimitUserRegistrationForm(request.session['registration_data'])
        return render(request, 'account/user_touroku-cfm.html', {'form': form})
    else:
        return redirect('UserCreateView')  # セッションデータがない場合は入力画面に戻る

# 新規登録確認
def TourokuConfirm(request):
    # if request.method == 'POST' and 'registration_data' in request.session:
    #     form = MelimitUserRegistrationForm(request.session['registration_data'])
    #     user = form.save(commit=False)
    #     print('登録きてるよ')
    #     user.backend = 'accounts.backends.MelimitUserModelBackend'
    #     login(request, user)
    #     del request.session['registration_data']
    #     return redirect('user:index')
    # else:
    #     return redirect('accounts:user_touroku')
    if request.method == 'POST' and 'registration_data' in request.session:
        form = MelimitUserRegistrationForm(request.session['registration_data'])
        if form.is_valid():
            print('登録きてるよ')
            # フォームのデータをセッションに保存
            # context = {
            #     'email': request.POST['email'],
            #     'password': request.POST['password'],
            #     'password_confirm': request.POST['password_confirm'],
            #     'username': request.POST['username'],
            #     'postal_code': request.POST['postal_code'],
            #     'prefecture': request.POST['prefecture'],
            #     'city': request.POST['city'],
            #     'address': request.POST['address'],
            #     'phone_number': request.POST['phone_number'],
            #     'taste': request.POST['taste'],
            # }
            # request.session['registration_data'] = request.POST
            # return render(request, 'account/user_touroku-cfm.html', context)
            user = form.save()
            print('登録成功')
                # backendを指定してログインさせる
            user.backend = 'accounts.backends.MelimitUserModelBackend'
            login(request, user)
            del request.session['registration_data']
            return redirect('user:index')
        else:
            print(form.errors)
            print('登録失敗')
            form_errors = form.errors
            return render(request, 'account/user_touroku.html', {'form': form,'form_errors':form_errors})
    else:
        return redirect('accounts:user_touroku')