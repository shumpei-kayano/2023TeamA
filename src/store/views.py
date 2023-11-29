from django.shortcuts import render
# formを使用するためにimport
from .forms import ProductForm, SaleForm
from accounts.mixins import MelimitModelMixin
from django.shortcuts import render, redirect
from accounts.forms import MelimitStoreLoginForm
from django.contrib.auth import authenticate, login

# Create your views here.
def index(request):
    print('インデックス')
    return render(request, 'store/index.html')
# 発送済み注文履歴(modelは注文履歴モデル、発送済みフラグtrueのものを表示)
def order_history_view(request):
    return render(request, 'store/order-history.html')
# 未発送注文一覧ページ(modelは注文履歴モデル、発送済みフラグfalseのものを表示)
def order_not_shipped_view(request):
    return render(request, 'store/order-not-shipped.html')
# 商品管理一覧ページ
def product_manage_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # productモデルの一覧表示
    products = user.melimitstore.product_set.all()
    print(f"products : {products}")
    for product in products:
        print(product.__dict__)
    # saleモデルの一覧表示
    sales = user.melimitstore.sale_set.all()
    print(f"sales : {sales}")
    for sale in sales:
        print(sale.__dict__)
    return render(request, 'store/test2.html', {'products': products, 'sales': sales, 'user': user,})
    # return render(request, 'store/product-manage.html')
# 一般新規登録
def create_general_purchase_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        product_form.instance.store = user.melimitstore
        # product_form.instance.storeを表示する
        print(product_form.instance.store)
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        print(sale_form.instance.store)
        sale_form.instance.product = product_form.instance
        # sale_form.instance.productを表示する
        print(sale_form.instance.product)
        if product_form.is_valid() and sale_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.sale_type = 'general_sales'
            sale.product = product
            sale.save()
            # ここでリダイレクトやメッセージ表示などを行う
        else:
            print('ビューのform.is_valid()失敗')
            print(product_form.errors)
            print(sale_form.errors)
    else:
        product_form = ProductForm()
        sale_form = SaleForm()

    return render(request, 'store/create-general-purchase.html', {'product_form': product_form, 'sale_form': sale_form, 'user': user, })

# 共同購入新規登録
def create_group_purchase_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        product_form.instance.store = user.melimitstore
        # product_form.instance.storeを表示する
        print(product_form.instance.store)
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        print(sale_form.instance.store)
        sale_form.instance.product = product_form.instance
        # sale_form.instance.productを表示する
        print(sale_form.instance.product)
        if product_form.is_valid() and sale_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.sale_type = 'melimit_sales'
            sale.product = product
            sale.save()
            # ここでリダイレクトやメッセージ表示などを行う
        else:
            print('ビューのform.is_valid()失敗')
            print(product_form.errors)
            print(sale_form.errors)
    else:
        product_form = ProductForm()
        sale_form = SaleForm()

    return render(request, 'store/create-group-purchase.html', {'product_form': product_form, 'sale_form': sale_form, 'user': user, })
def detail_general_view(request):
    return render(request, 'store/detail-general.html')
def detail_group_view(request):
    return render(request, 'store/detail-group.html')

# ログイン処理
def store_login_view(request):
    user = request.user
    # username = user.username
    # model_name = user.__class__.__name__
    # instance_name = type(user).__name__
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
                print('ログイン成功')
                return redirect('store:store_base')
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

# ログイン後の店舗管理画面
def store_base_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # お客さんがログインしようとしたときの処理
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
    print(f'user: {user}')
    print(f'model_name: {model_name}')
    return render(request, 'store/base.html', {
        'user': user,
        'model_name': model_name,
        'instance_name': instance_name,
    })

# 販売&商品登録
# 未使用
def create_product_and_sale(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        product_form.instance.store = user.melimitstore
        # product_form.instance.storeを表示する
        print(product_form.instance.store)
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        print(sale_form.instance.store)
        sale_form.instance.product = product_form.instance
        # sale_form.instance.productを表示する
        print(sale_form.instance.product)
        if product_form.is_valid() and sale_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.sale_type = 'general_sales'
            sale.product = product
            sale.save()
            # ここでリダイレクトやメッセージ表示などを行う
        else:
            print('ビューのform.is_valid()失敗')
            print(product_form.errors)
            print(sale_form.errors)
    else:
        product_form = ProductForm()
        sale_form = SaleForm()

    return render(request, 'store/test.html', {'product_form': product_form, 'sale_form': sale_form, 'user': user, })

# productモデルとsaleモデルの一覧表示
def product_and_sale_list(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # productモデルの一覧表示
    products = user.melimitstore.product_set.all()
    print(f"products : {products}")
    for product in products:
        print(product.__dict__)
    # saleモデルの一覧表示
    sales = user.melimitstore.sale_set.all()
    print(f"sales : {sales}")
    for sale in sales:
        print(sale.__dict__)
    return render(request, 'store/test2.html', {'products': products, 'sales': sales, 'user': user,})

# productモデルの登録
# 未使用
def create_product(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    model_name = user.__class__.__name__
    # userのmelimitstoreを表示する
    print(user.melimitstore.id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        # print(form)
        # print(f"ユーザー: {user}")
        # print(f"メリミット: {user.melimitstore}")
        # melimitstoreインスタンスからstoreフィールドに設定するidを取得する
        form.instance.store = user.melimitstore
        # print(f"form.instance.store: {form.instance.store}")
        # userがmelimitstoreかどうかをtrue/falseで表示する
        # print(f"ユーザーがmelimitstoreかどうか: {hasattr(user, 'melimitstore')}")
        # print(f"ユーザーのクラス: {user.__class__.__name__}")
        if form.is_valid():
            print('ビューのform.is_valid()成功')
            form.save()
            # ここでリダイレクトやメッセージ表示などを行う
        else:
            print('ビューのform.is_valid()失敗')
            print(form.errors)
    else:
        form = ProductForm()
        # 初回表示時にstoreフィールドにuserのmelimitstoreのidを入れる場合
        # form = ProductForm(initial={'store': user.melimitstore.id})
        # print(f"Storeの初期値: {form.initial['store']}")
        print(form)

    return render(request, 'store/test.html', {'product_form': form, 'user': user, 'model_name': model_name})