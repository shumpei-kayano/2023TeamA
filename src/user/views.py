from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm
from accounts.models import MelimitStore, MelimitUser
from accounts.mixins import MelimitModelMixin

# Create your views here.
# @login_required
def index(request):
    print(request.user)
    if request.user.is_authenticated:
        if request.user.user_type == 'melimit_user' :
            user_id = request.user.id
            # user_id = request.session.get('user_id')
            print(f'user_id: {user_id}')
            user = MelimitUser.objects.get(id=user_id)
            print(f'user: {user}')
            return render(request, 'user/index.html', {'user': user})
        else:
            return redirect('user:omae_store')
    else:
        return render(request, 'user/index.html')
    # print('index_________')
    # print(request.user.user_id)
    # return render(request, 'user/index.html')
def login_view(request):
    return render(request, 'user/login.html')


    
    # return render(request, 'user/index.html')

def anai(request):
    user = request.user
    username = user.username
    model_name = user.__class__.__name__
    instance_name = type(user).__name__
    return render(request, 'user/ana_ana.html', {'model_name': model_name, 'instance_name': instance_name})

def store_base_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if user.__class__.__name__ == 'MelimitUser':
        return redirect('user:omae_user')
    # user = request.user
    # store_id = request.session.get('store_id')
    # print(f'store_id: {store_id}')
    # try:
    #     user = MelimitStore.objects.get(id=store_id)
    # except MelimitStore.DoesNotExist:
    #     return redirect('user:omae_user')
    # model_name = request.session.get('model_name')
    instance_name = request.session.get('instance_name')
    model_name = user.__class__.__name__
    print(f'user.__class__.__name__: {user.__class__.__name__}')
    # userのsite_urlを取得
    site_url = user.site_url
    print(f'site_url: {site_url}')
    return render(request, 'store/base.html', {
        'user': user,
        'model_name': model_name,
        'instance_name': instance_name,
    })

def store_login_view(request):
    user = request.user
    username = user.username
    model_name = user.__class__.__name__
    instance_name = type(user).__name__
    # return render(request, 'store/base.html', {'model_name': model_name, 'instance_name': instance_name})
    if request.method == 'POST':
        form = MelimitStoreLoginForm(request.POST)
        print('store_login_view')
        # フォームに入力された値を出力してみる
        print(f'Username: {form.data.get("username")}')
        print(f'email: {form.data.get("email")}')
        print(f'Password: {form.data.get("password")}')
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password, backend='accounts.backends.MelimitStoreModelBackend')
            # 適用される認証バックエンドを出力してみる
            # print(f'backend: {user.backend}')
            # ユーザーの情報を出力してみる
            # print(f'Username: {user.username}')
            if user is not None:
                login(request, user)
                return redirect('user:store_base')
            else:
                # フォームが無効な場合の処理をここに書く
                print('pass')
                form.add_error(None, 'メールアドレスまたはパスワードが間違っています。')  # ユーザーが認証できない場合のエラーメッセージ
                return render(request, 'account/store_login.html', {'form': form})
        else:
            print(form.errors)
            print('rogin-error')
    else:
        # form = MelimitStoreLoginForm()

        if 'backend' in request.session:
            del request.session['backend']
        request.session['backend'] = 'accounts.backends.MelimitStoreModelBackend'
        print(f'session: {request.session}')
        print(f'session: {dict(request.session)}')

        return render(request, 'account/store_login.html', {'form': form})

# ユーザー側から店舗がログインしようとしたときのビュー
def omae_store(request):
    logout(request)
    return render(request, 'account/userlogin_storeerror.html')
# 店舗側からユーザーがログインしようとしたときのビュー
def omae_user(request):
    logout(request)
    return render(request, 'account/storelogin_usererror.html')

def sinki(request):
    print('sinki_________')
    return render(request, 'user/sinki.html')