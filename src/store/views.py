from django.shortcuts import render
# formを使用するためにimport
from .forms import ProductForm, SaleForm
from accounts.mixins import MelimitModelMixin

# Create your views here.
def index(request):
    return render(request, 'store/index.html')
def order_history_view(request):
    return render(request, 'store/order-history.html')
def order_not_shipped_view(request):
    return render(request, 'store/order-not-shipped.html')
def product_manage_view(request):
    return render(request, 'store/product-manage.html')
def create_general_purchase_view(request):
    return render(request, 'store/create-general-purchase.html')
def create_group_purchase_view(request):
    return render(request, 'store/create-group-purchase.html')

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