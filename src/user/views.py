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
def explain_view(request):
    return render(request, 'user/explain.html')
def contact_view(request):
    return render(request, 'user/contact.html')



    # return render(request, 'user/index.html')

def anai(request):
    user = request.user
    username = user.username
    model_name = user.__class__.__name__
    instance_name = type(user).__name__
    return render(request, 'user/ana_ana.html', {'model_name': model_name, 'instance_name': instance_name})

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

# 一般商品詳細
def general_products_detail(request):
    return render(request, 'user/general-products_detail.html')