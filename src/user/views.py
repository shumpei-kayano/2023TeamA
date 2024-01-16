from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm
from accounts.models import MelimitStore, MelimitUser
from accounts.mixins import MelimitModelMixin
from store.models import Sale, Product
import random
# Create your views here.
# @login_required
def index(request):
    print(request.user)
    # ログインしているか
    if request.user.is_authenticated:
        # ログインしているのがユーザーか
        if request.user.user_type == 'melimit_user' :
            user_id = request.user.id
            # user_id = request.session.get('user_id')
            print(f'user_id: {user_id}')
            user = MelimitUser.objects.get(id=user_id)
            print(f'user: {user}')
            user_taste = user.taste  # ユーザーの好みを取得
            matching_sales = Sale.objects.filter(product__product_category=user_taste).order_by('?')[:3]  # ユーザーの好みに合った商品をランダムに3つ取得
            
            # matching_sales = Sale.objects.filter(product__product_category=user_taste)  # ユーザーの好みに合った商品を取得
            # random_sale = random.choice(matching_sales)  # ランダムに1つの商品を選択
            categories = Product.TASTE_CHOICES #商品をカテゴリーごとに取得
            # random_sale.sale_priceとrandom_sale.product.product_price
            
            sales_by_category = {category[0]: Sale.objects.filter(product__product_category=category[0]) for category in categories}
            # return render(request, 'index.html', {'random_sale': random_sale})
            return render(request, 'user/index.html', {'user': user,'random_sales': matching_sales,'sales_by_category': sales_by_category})
        else:
            return redirect('user:omae_store')
    else:
        # 商品をカテゴリーごとに取得
        categories = Product.TASTE_CHOICES
        sales_by_category = {category[0]: Sale.objects.filter(product__product_category=category[0]) for category in categories}
        # return render(request, 'sales_list.html', {'sales_by_category': sales_by_category})
        return render(request, 'user/index.html', {'sales_by_category': sales_by_category})
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

# お問い合わせ確認
def contact_confirm(request):
    context = {
        'name': request.POST['name'],
        'company': request.POST['company'],
        'email': request.POST['email'],
        'phone': request.POST['phone'],
        'message': request.POST['message'],
    }
     # フォームのデータをセッションに保存
    request.session['contact_data'] = request.POST
    return render(request, 'user/contact-cfm.html', context)

# お問い合わせ送信完了
def contact_complete(request):
    return render(request, 'user/contact-complete.html')

# 一般商品一覧
def all_products_general(request):
    return render(request, 'user/general-products.html')

# 共同購入商品一覧
def all_products_joint(request):
    return render(request, 'user/joint-products.html')

# 一般商品詳細
def general_products_detail(request):
    return render(request, 'user/general-products_detail.html')

# 共同購入商品詳細
def joint_products_detail(request):
    return render(request, 'user/joint-products_detail.html')

# カート
def cart(request):
    return render(request, 'user/cart.html')
#お知らせ詳細
def notice(request):
    return render(request, 'user/notice.html')

# 注文詳細
def history(request):
    return render(request, 'user/history.html')
#注文完了
def order_completed(request):
    return render(request, 'user/order-completed.html')
    

# お気に入り
def favorite(request):
    return render(request, 'user/favorite.html')

# パスワード設定用メール送信完了
def pass_mail(request):
    return render(request, 'user/pass-mail.html')
