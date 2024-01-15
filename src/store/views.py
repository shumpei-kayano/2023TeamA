from django.shortcuts import render
# formを使用するためにimport
from .forms import ProductForm, SaleForm, ThresholdForm, MelimitStoreEditForm
from accounts.mixins import MelimitModelMixin
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import MelimitStoreLoginForm
from django.contrib.auth import authenticate, login
from .models import Product, Sale, Threshold
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponseBadRequest

# Create your views here.
def index(request):
    print('インデックス')
    return render(request, 'store/index.html')
# 発送済み注文履歴(modelは注文履歴モデル、発送済みフラグtrueのものを表示)
def order_history_view(request):
    return render(request, 'store/order-history.html')
# 発送済み注文履歴ページの中身
def order_history_content_view(request):
    return render(request, 'store/order-history-content.html')
# 未発送注文一覧ページ(modelは注文履歴モデル、発送済みフラグfalseのものを表示)
def order_not_shipped_view(request):
    return render(request, 'store/order-not-shipped.html')
# 未発送注文一覧ページの中身
def order_not_shipped_content_view(request):
    return render(request, 'store/order-not-shipped-content.html')
# パスワード再設定用のメール送信ページ
def pass_mail_view(request):
    return render(request, 'store/pass-mail.html')
# 店舗情報設定ページ
def store_info_view(request):
    return render(request, 'store/store-info.html')

# 店舗情報設定ページの編集
def store_info_edit_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    print(f"店舗情報設定ページの編集のuser : {user}")
    print(request.method)
    if request.method == 'POST':
        print('postです')
        form = MelimitStoreEditForm(request.POST, instance=user.melimitstore)
        if form.is_valid():
            form.save()
            return redirect('store:store-info')
    else:
        print('postじゃないです')
        form = MelimitStoreEditForm(instance=user.melimitstore)
    return render(request, 'store/store-info-edit.html', {'form': form, 'user': user,})

# 店舗の新規登録ページ
def store_create_view(request):
    return render(request, 'store/store-create.html')


# 商品管理一覧ページ
# 検証用(render先が仮)
# 実際のページに適用済み
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
    return render(request, 'store/product-manage.html', {'products': products, 'sales': sales, 'user': user,})
    # return render(request, 'store/product-manage.html')

# 商品詳細ページ
# 検証用
def sale_detail_view(request, pk):
    if pk > Sale.objects.latest('id').id:
        return render(request, 'store/test3_error.html')
    sale = get_object_or_404(Sale, id=pk)
    # ログイン中のユーザーだけが商品詳細ページを見れるようにする
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    print(f"pk : {pk}")
    print(f"user.id : {user.id}")
    print(f"user.melimitstore : {user.melimitstore}")
    print(f"sale.store : {sale.store}")
    print(f"trueならsale取得、詳細表示する : {user.melimitstore == sale.store}")
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
        elif sale.sale_type == 'melimit_sales':
            threshold = Threshold.objects.get(sale=sale)
            print(f"threshold : {threshold}")
            return render(request, 'store/detail-group.html', {'sale': sale, 'threshold': threshold, 'user': user,})
    else:
        print('ログインしていません')
        # エラーページを表示する
        return render(request, 'store/test3_error.html')

# 一般新規登録
def create_general_purchase_view(request):
    print('view:create_general_purchase_view')
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        product_form.instance.store = user.melimitstore
        # product_form.instance.storeを表示する
        print(f"product_form.instance.store: {product_form.instance.store}")
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        print(f"sale_form.instance.store: {sale_form.instance.store}")
        sale_form.instance.product = product_form.instance
        # sale_form.instance.productを表示する
        print(f"sale_form.instance.product: {sale_form.instance.product}")
        if product_form.is_valid() and sale_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.sale_type = 'general_sales'
            sale.product = product
            sale.save()
            return redirect('store:product-manage')
        else:
            print('一般新規登録ビューのform.is_valid()失敗')
            print(f"product_form.errors: {product_form.errors}")
            print(f"sale_form.errors: {sale_form.errors}")
    else:
        product_form = ProductForm()
        sale_form = SaleForm()
    return render(request, 'store/create-general-purchase.html', {'product_form': product_form, 'sale_form': sale_form, 'user': user, })

# 詳細ページから遷移した商品編集ページ(一般)
def detail_general_edit_view(request, product_id):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    product = get_object_or_404(Product, id=product_id, store=user.melimitstore)
    sale = get_object_or_404(Sale, product=product, store=user.melimitstore)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        sale_form = SaleForm(request.POST, instance=sale, request=request)
        if product_form.is_valid() and sale_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.product = product
            sale.sale_type = 'general_sales'
            sale.save()
            print('完了')
            # 編集が完了したら、適切なページにリダイレクトする
            return redirect('store:product-manage')
        else:
            print('失敗')
    else:
        product_form = ProductForm(instance=product)
        sale_form = SaleForm(instance=sale)
        print(f"product_form: {product_form}")
        # print(f"sale_form: {sale_form}")
        print(f"編集product: {product.__dict__}")
        print(f"編集sale: {sale.__dict__}")
        print(product.product_name)

    return render(request, 'store/detail-general-edit.html', {'product_form': product_form, 'sale_form': sale_form, 'product': product, 'user': user})
    # return render(request, 'store/detail-general-edit.html')


# 共同購入新規登録
def create_group_purchase_view(request):
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        sale_form = SaleForm(request.POST)
        threshold_form = ThresholdForm(request.POST)
        product_form.instance.store = user.melimitstore
        # product_form.instance.storeを表示する
        print(product_form.instance.store)
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        print(sale_form.instance.store)
        sale_form.instance.product = product_form.instance
        # sale_form.instance.productを表示する
        print(sale_form.instance.product)
        # threshold_formの登録とthresholdの外部キーにsaleのidを設定する
        if product_form.is_valid() and sale_form.is_valid() and threshold_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.product = product
            sale.sale_type = 'melimit_sales'
            sale.save()
            threshold = threshold_form.save(commit=False)
            threshold.sale = sale
            threshold.save()
            return redirect('store:product-manage')
        else:
            print('ビューのform.is_valid()失敗')
            print(product_form.errors)
            print(sale_form.errors)
            print(threshold_form.errors)
    else:
        product_form = ProductForm()
        sale_form = SaleForm()
        threshold_form = ThresholdForm()

    return render(request, 'store/create-group-purchase.html', {'product_form': product_form, 'sale_form': sale_form, 'threshold_form': threshold_form, 'user': user, })

    return render(request, 'store/create-group-purchase.html', {'product_form': product_form, 'sale_form': sale_form, 'user': user, })

# 詳細ページから遷移した商品編集ページ(共同)
def detail_group_edit_view(request, product_id):
    print(f"共同product_id: {product_id}")
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    product = get_object_or_404(Product, id=product_id, store=user.melimitstore)
    sale = get_object_or_404(Sale, product=product, store=user.melimitstore)
    threshold = get_object_or_404(Threshold, sale=sale)
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        print('1番')
        sale_form = SaleForm(request.POST, instance=sale, request=request)
        print('2番')
        threshold_form = ThresholdForm(request.POST, instance=threshold)
        product_form.instance.store = user.melimitstore
        if product_form.is_valid() and sale_form.is_valid() and threshold_form.is_valid():
            product = product_form.save()
            sale = sale_form.save(commit=False)
            sale.sale_type = 'melimit_sales'
            sale.product = product
            sale.save()
            threshold = threshold_form.save(commit=False)
            threshold.sale = sale
            threshold.save()
            print('完了')
            # 編集が完了したら、適切なページにリダイレクトする
            return redirect('store:product-manage')
        else:
            # print(f"product_form: {product_form.is_valid()}")
            # print(f"productエラー: {product_form.errors}")
            # print(f"sale_form: {sale_form.is_valid()}")
            # print(f"saleエラー: {sale_form.errors}")
            # print(f"threshold_form: {threshold_form.is_valid()}")
            # print(f"saleエラー: {sale_form.errors}")
            print(f"product: {product.__dict__}")
            print(f"sale: {sale.__dict__}")
            print(f"threshold: {threshold.__dict__}")
            print('失敗')
    else:
        product_form = ProductForm(instance=product)
        sale_form = SaleForm(instance=sale)
        threshold_form = ThresholdForm(instance=threshold)
        print(f"threshold_form: {threshold_form}")

    return render(request, 'store/detail-group-edit.html', {'product_form': product_form, 'sale_form': sale_form, 'threshold_form': threshold_form,'product': product,'user': user})

# 商品詳細ページ(一般)
def detail_general_view(request):
    return render(request, 'store/detail-general.html')
# 商品詳細ページ(共同)
def detail_group_view(request):
    return render(request, 'store/detail-group.html')
# 詳細ページから遷移した商品編集ページ(共同)
# def detail_group_edit_view(request):
#     return render(request, 'store/detail-group-edit.html')

# ログイン処理
def store_login_view(request):
    print('view:store_login_view')
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
                return redirect('store:index')
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
    print('view:store_base_view')
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # melimitstore以外のユーザーを弾く
    # if user.__class__.__name__ == 'MelimitUser':
    if user.__class__.__name__ != 'MelimitStore':
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
    return render(request, 'store/index.html', {
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
# 検証用
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

# 商品削除
def product_and_sale_delete_view(request, pk):
    print('削除ビュー')
    if request.method == 'POST':
        # pkを元にproductとsaleを取得する
        product = get_object_or_404(Product, id=pk)
        sale = get_object_or_404(Sale, product=product)
        mixin = MelimitModelMixin()
        mixin.request = request
        user = mixin.get_melimitmodel_user()
        print('削除postです')
        print(f"product: {product}")
        print(f"sale: {sale}")
        print(f"user: {user}")
        # 取得しているproductとsaleがログイン中のユーザーのものかを確認する
        if product.store == user.melimitstore and sale.store == user.melimitstore:
            product.delete()
            print('削除完了')
            return redirect('store:product-manage')
    else:
        return HttpResponseBadRequest()

# 商品複数一括削除
class ProductAndSaleDeleteView(View):
    def get(self, request, *args, **kwargs):
        product_ids = request.GET.getlist('product_ids')  # 選択した商品のIDを取得
        print(f"product_ids : {product_ids}")
        products = Product.objects.filter(id__in=product_ids)
        sales = []
        for product in products:
            product_sales = product.sale_set.all()  # Productに関連するSaleを取得
            sales.extend(product_sales)  # Saleをリストに追加
        print(f"products : {products}")
        print(f"sales : {sales}")
        return render(request, 'store/test4.html', {'products': products})

    def post(self, request, *args, **kwargs):
        product_ids = request.POST.getlist('product_ids')  # 選択した商品のIDを取得
        print(f"del_product_ids : {product_ids}")
        for product_id in product_ids:
            print(f"delete : {product_id}")
            self.delete_product_and_sale(product_id)
        return redirect('store:test2')

    def delete_product_and_sale(self, product_id):
        # productモデルの削除
        product = get_object_or_404(Product, id=product_id)
        print(f"del_product : {product}")
        print(f"del_id : {product_id}")
        product.delete()
    # productはsaleの外部キーなので、productを削除するとsaleも削除される
    # また、thresholdはsaleの外部キーなので、saleを削除するとthresholdも削除される
    # そのため、productを削除すると関連するsaleとthresholdも削除される
    # モデル定義でon_delete=models.CASCADEを指定しているため

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