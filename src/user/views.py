from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm

# Create your views here.
# @login_required
def index(request):
    print('index_________')
    return render(request, 'user/index.html')
def login_view(request):
    return render(request, 'user/login.html')
def explain_view(request):
    return render(request, 'user/explain.html')


    
    # return render(request, 'user/index.html')

def anai(request):
    user = request.user
    username = user.username
    model_name = user.__class__.__name__
    instance_name = type(user).__name__
    return render(request, 'user/ana_ana.html', {'model_name': model_name, 'instance_name': instance_name})

def store_base_ikuyo_view(request):
    model_name = request.session.get('model_name')
    instance_name = request.session.get('instance_name')
    # htmlを返すだけ
    return render(request, 'store/base.html', {
        'model_name': model_name,
        'instance_name': instance_name,
    })

def store_base_view(request):
    user = request.user
    username = user.username
    model_name = user.__class__.__name__
    instance_name = type(user).__name__
    # return render(request, 'store/base.html', {'model_name': model_name, 'instance_name': instance_name})
    if request.method == 'POST':
        form = MelimitStoreLoginForm(request.POST)
        print('store_base_view')
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
                return redirect('user:store_base_ikuyo')
            else:
                # フォームが無効な場合の処理をここに書く
                print('pass')
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

# メリミットとは
def what_melimit(request):
    return render(request, 'user/explain.html')

# お問い合わせ
def contact(request):
    return render(request, 'user/contact.html')

# 一般商品一覧
def all_products_general(request):
    return render(request, 'user/general-products.html')

# 共同購入商品一覧
def all_products_joint(request):
    return render(request, 'user/joint-products.html')