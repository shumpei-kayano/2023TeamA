from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm
from accounts.models import MelimitStore, MelimitUser
from accounts.mixins import MelimitModelMixin
from store.models import Sale, Product
import random
from django.db.models import Q
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
            print(user_taste)
            matching_sales = Sale.objects.filter(product__product_category=user_taste).order_by('?')[:3]  # ユーザーの好みに合った商品をランダムに3つ取得
            print(matching_sales)
            # matching_sales = Sale.objects.filter(product__product_category=user_taste)  # ユーザーの好みに合った商品を取得
            # random_sale = random.choice(matching_sales)  # ランダムに1つの商品を選択
            categories = Product.TASTE_CHOICES #商品をカテゴリーごとに取得
            # random_sale.sale_priceとrandom_sale.product.product_price
            print(categories)
            sales_by_category = {category[0]: Sale.objects.filter(product__product_category=category[0]) for category in categories}
            # return render(request, 'index.html', {'random_sale': random_sale})
            print(sales_by_category)
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

# 一般商品一覧
def all_products_general(request):
    sales_by_choices = {}
    for choice, _ in Sale.SALE_CHOICES:
        sales_by_choices[choice] = Sale.objects.filter(sale_type=choice)
    for i in sales_by_choices['general_sales']:
        # iの他の情報をprintしたい
        print(i.product.product_name)
        print(i.sale_price)
        print(i)
        print(i.pk)
        print(1)
    sales = sales_by_choices['general_sales']
    # return render(request, 'user/general-products.html')
    return render(request, 'user/general-products.html' , {'sales_by_choices': sales_by_choices, 'sales': sales})

# 共同購入商品一覧
def all_products_joint(request):
    return render(request, 'user/joint-products.html')

# 一般商品詳細
def general_products_detail(request,pk):
    #detailに必要なデータをここで取得する
    #値段
    #商品名
    #割引率
    #商品説明
    #商品画像
    #商品のカテゴリー
    #送料
    #在庫数
    #商品から店舗情報
    sale = Sale.objects.get(id=pk)
    print(sale.stock)
    print(sale.product.store)
    print(sale.product.store.site_url)
    print(sale.product.store.store_image)
    print(sale.product.store.email)
    print(sale.product.product_category)
    #商品と同じ店舗の商品と、同じカテゴリーの商品を取得する
    # sales = Sale.objects.filter(Q(sale_type='general_sales')| Q(sale_price__gt=1000))
    # related_sales = Sale.objects.filter(Q(product__store=sale.product.store) | Q(product__category=sale.product.product_category))
    related_sales = Sale.objects.filter(Q(product__store=sale.product.store) | Q(product__product_category=sale.product.product_category)).order_by('?')[:3]
    print(related_sales)
    return render(request, 'user/general-products_detail.html', {'sale': sale, 'related_sales':related_sales})

def sale_detail_view(request, pk):
    
    sale = get_object_or_404(Sale, id=pk)
    # ログイン中のユーザーだけが商品詳細ページを見れるようにする

    if user.is_authenticated:
        try:
            # saleのpkとmelimitstoreオブジェクトの組み合わせが正しい場合のみDBからsaleを取得する
            # つまり、urlを直接入力しても他店のsaleは取得できない
            sale = Sale.objects.get(id=pk, store=user.melimitstore)
        except ObjectDoesNotExist:
            print('ログインしているmelimitstoreと取得したいsaleのmelimitstoreが一致しません')
            return render(request, 'store/test3_error.html')
        if sale.sale_type == 'general_sales':
            return render(request, 'store/detail-general.html', {'sale': sale, 'user': user,})

# 共同購入商品詳細
def joint_products_detail(request):
    return render(request, 'user/joint-products_detail.html')