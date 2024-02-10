from django.shortcuts import render
# formを使用するためにimport
from .forms import ProductForm, SaleForm, ThresholdForm, MelimitStoreEditForm
from accounts.mixins import MelimitModelMixin
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import MelimitStoreLoginForm
from django.contrib.auth import authenticate, login
from .models import Product, Sale, Threshold
from user.models import OrderHistory
from accounts.models import MelimitStore
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import View
from django.http import HttpResponseBadRequest
from django.db.models import Sum
from django.db.models.functions import TruncYear, TruncMonth, TruncDay, ExtractYear
from datetime import datetime, timedelta
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

# Create your views here.
def index(request):
    # ログインしているユーザーを取得する
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # modelからデータを取得する
    print(f"user : {user.__dict__}")
    print(f"user.customuser_ptr_id : {user.customuser_ptr_id}")
    # store = MelimitStore.objects.get(user=user.customuser_ptr_id)

    # 更新ボタンが押されたか、またはセッションデータが存在しない場合にデータを取得
    if 'update' in request.POST or 'context_co2_amount' not in request.session or 'context_total_data' not in request.session:
        # 現在の年、月、日を取得
        now = timezone.now()

        # 4年前から現在までの年間のデータを取得
        yearly_data = OrderHistory.objects.filter(
            orderhistory_store_id=user.customuser_ptr_id, 
            order_date__year__gte=now.year-4
        ).annotate(
            year=ExtractYear('order_date')
        ).values(
            'year'
        ).annotate(
            total_co2=Sum('co2'), 
            total_amount=Sum('amount')
        ).order_by('year')
        print(f"最初のyearly_data : {yearly_data}")
        # relativedeltaを使用した方が、年の計算が楽になるかもしれない
        # yearly_data_dict = {year: {'total_co2': 0, 'total_amount': 0} for year in range(now.year-4, now.year+1)}
        # relativedeltaを使用して、年の計算を行う
        yearly_data_dict = {}
        for i in range(4, -1, -1):
            year = (now - relativedelta(years=i)).year
            yearly_data_dict[year] = {'total_co2': 0, 'total_amount': 0}
        print(f"空のyearly_data_dict : {yearly_data_dict}")
        for data in yearly_data:
            yearly_data_dict[data['year']] = {'total_co2': data['total_co2'], 'total_amount': data['total_amount']}
        print(f"yearly_data_dict : {yearly_data_dict}")
        print(f"yearly_data_dict[2020]['total_co2'] : {yearly_data_dict[2020]['total_co2']}")
        # yearly_data_dictの'total_co2'リストと'total_amount'リストを作成
        yearly_data_co2_list = [data['total_co2'] for year, data in yearly_data_dict.items()]
        # 要素を全て整数型に変換
        yearly_data_co2_list = list(map(int, yearly_data_co2_list))
        print(f"yearly_data_co2_list : {yearly_data_co2_list}")
        yearly_data_amount_list = [data['total_amount'] for year, data in yearly_data_dict.items()]
        # 要素を全て整数型に変換
        yearly_data_amount_list = list(map(int, yearly_data_amount_list))
        print(f"yearly_data_amount_list : {yearly_data_amount_list}")
        # yearly_data_list = [{'year': year, 'total_co2': data['total_co2'], 'total_amount': data['total_amount']} for year, data in yearly_data_dict.items()]
        # print(f"yearly_data_list : {yearly_data_list}")

        # 1年前から現在までの月間のデータを取得
        monthly_data = OrderHistory.objects.filter(
            orderhistory_store_id=user.customuser_ptr_id, 
            order_date__gte=now-timedelta(days=365)
            ).annotate(
                month=TruncMonth('order_date')
            ).values(
                'month'
            ).annotate(
                total_co2=Sum('co2'), 
                total_amount=Sum('amount')
            ).order_by('month')
        print(f"最初のmonthly_data : {monthly_data}")
        monthly_data_dict = {}
        # 今月を最後の要素として過去11ヶ月分のデータを格納する空の辞書を作成
        # relativedeltaを使用した方が、月の計算が楽になるかもしれない
        # for month in range(now.month-11, now.month+1):
        #     if month <= 0:
        #         month += 12
        #     monthly_data_dict[month] = {'total_co2': 0, 'total_amount': 0}
        # relativedeltaを使用して、月の計算を行う
        # 記述によっては数年前の等の計算も自動で行ってくれるはず
        for i in range(11, -1, -1):
            month = (now - relativedelta(months=i)).month
            monthly_data_dict[month] = {'total_co2': 0, 'total_amount': 0}
        print(f"空のmonthly_data_dict : {monthly_data_dict}")
        for data in monthly_data:
            monthly_data_dict[data['month'].month] = {'total_co2': data['total_co2'], 'total_amount': data['total_amount']}
        print(f"monthly_data_dict : {monthly_data_dict}")
        # monthly_data_dictの'total_co2'リストと'total_amount'リストを作成
        monthly_data_co2_list = [data['total_co2'] for month, data in monthly_data_dict.items()]
        # 要素を全て整数型に変換
        monthly_data_co2_list = list(map(int, monthly_data_co2_list))
        print(f"monthly_data_co2_list : {monthly_data_co2_list}")
        monthly_data_amount_list = [data['total_amount'] for month, data in monthly_data_dict.items()]
        # 要素を全て整数型に変換
        monthly_data_amount_list = list(map(int, monthly_data_amount_list))
        print(f"monthly_data_amount_list : {monthly_data_amount_list}")

        # 1週間前から現在までの日間のデータを取得
        daily_data = OrderHistory.objects.filter(
            orderhistory_store_id=user.customuser_ptr_id, 
            order_date__gte=now-timedelta(days=7)
            ).annotate(
                day=TruncDay('order_date')
                ).values(
                    'day'
                ).annotate(
                    total_co2=Sum('co2'), 
                    total_amount=Sum('amount')
                ).order_by('day')
        print(f"最初のdaily_data : {daily_data}")
        # 今日を最後の要素として過去6日分のデータを格納する空の辞書を作成
        daily_data_dict = {}
        # timedelta(days=i)でi日前の日付を取得、月初めや閏年の場合は自動で調整される
        for i in range(6, -1, -1):
            day = (now - timedelta(days=i)).day
            daily_data_dict[day] = {'total_co2': 0, 'total_amount': 0}
        print(f"空のdaily_data_dict : {daily_data_dict}")
        for data in daily_data:
            daily_data_dict[data['day'].day] = {'total_co2': data['total_co2'], 'total_amount': data['total_amount']}
        print(f"daily_data_dict : {daily_data_dict}")
        # daily_data_dictの'total_co2'リストと'total_amount'リストを作成
        daily_data_co2_list = [data['total_co2'] for day, data in daily_data_dict.items()]
        # 要素を全て整数型に変換
        daily_data_co2_list = list(map(int, daily_data_co2_list))
        print(f"daily_data_co2_list : {daily_data_co2_list}")
        daily_data_amount_list = [data['total_amount'] for day, data in daily_data_dict.items()]
        # 要素を全て整数型に変換
        daily_data_amount_list = list(map(int, daily_data_amount_list))
        print(f"daily_data_amount_list : {daily_data_amount_list}")

        # melimitstoreかつ、sale_type='general_sales'の商品の総数を取得
        total_general = Sale.objects.filter(store=user.melimitstore, sale_type='general_sales').count()
        print(f"total_Sale : {total_general}")
        # melimitstoreかつ、sale_type='melimit_sales'の商品の総数を取得
        total_melimit = Sale.objects.filter(store=user.melimitstore, sale_type='melimit_sales').count()
        print(f"total_melimit : {total_melimit}")
        total_shipped = OrderHistory.objects.filter(orderhistory_store=user.melimitstore, is_shipped=True).count()
        print(f"total_shipped : {total_shipped}")
        total_not_shipped = OrderHistory.objects.filter(orderhistory_store=user.melimitstore, is_shipped=False).count()
        print(f"total_not_shipped : {total_not_shipped}")

        context_co2_amount = {
            'yearly_data_co2_list': yearly_data_co2_list,
            'yearly_data_amount_list': yearly_data_amount_list,
            'monthly_data_co2_list': monthly_data_co2_list,
            'monthly_data_amount_list': monthly_data_amount_list,
            'daily_data_co2_list': daily_data_co2_list,
            'daily_data_amount_list': daily_data_amount_list,
        }
        context_total_data = {
            'total_general': total_general,
            'total_melimit': total_melimit,
            'total_shipped': total_shipped,
            'total_not_shipped': total_not_shipped,
        }
        # セッションにデータを保存
        request.session['context_co2_amount'] = context_co2_amount
        print(f"セッションに保存したcontext_co2_amount : {context_co2_amount}")
        request.session['context_total_data'] = context_total_data
    else:
        # セッションからデータを取得
        context_co2_amount = request.session['context_co2_amount']
        print(f"セッションから取得したcontext_co2_amount : {context_co2_amount}")
        context_total_data = request.session['context_total_data']
    print(f"セッションから取得したcontext_total_data : {context_total_data}")
    print('インデックス')
    return render(request, 'store/index.html', {'user': user, 'context_co2_amount': context_co2_amount, 'context_total_data': context_total_data, })

# 発送済み注文履歴(modelは注文履歴モデル、発送済みフラグtrueのものを表示)
def order_history_view(request):
    # ログインしているユーザーの注文履歴を取得する
    mixin = MelimitModelMixin()
    mixin.request = request
    store = mixin.get_melimitmodel_user()
    order_histories = OrderHistory.objects.filter(orderhistory_store=store)
    print(f"order_histories : {order_histories}")
    # order_historiesからその"発送済みフラグ"がfalseのデータを全て取得する
    order_histories = order_histories.filter(is_shipped=True)
    return render(request, 'store/order-history.html', {'order_histories': order_histories,})

# 発送済み注文履歴ページの中身
def order_history_content_view(request, order_id):
    # URLから注文IDを取得し、そのIDに対応するOrderHistoryのインスタンスを取得する
    order_history = get_object_or_404(OrderHistory, id=order_id)
    return render(request, 'store/order-history-content.html', {'order_history': order_history,})

# 未発送注文一覧ページ(modelは注文履歴モデル、発送済みフラグfalseのものを表示)
def order_not_shipped_view(request):
    # ログインしているユーザーの注文履歴を取得する
    mixin = MelimitModelMixin()
    mixin.request = request
    store = mixin.get_melimitmodel_user()
    order_histories = OrderHistory.objects.filter(orderhistory_store=store)
    print(f"order_histories : {order_histories}")
    # order_historiesからその"発送済みフラグ"がfalseのデータを全て取得する
    order_histories = order_histories.filter(is_shipped=False)
    return render(request, 'store/order-not-shipped.html', {'order_histories': order_histories,})

# 未発送注文一覧ページの中身
def order_not_shipped_content_view(request, order_id):
    # URLから注文IDを取得し、そのIDに対応するOrderHistoryのインスタンスを取得する
    order_history = get_object_or_404(OrderHistory, id=order_id)
    return render(request, 'store/order-not-shipped-content.html', {'order_history': order_history,})

# 注文履歴を未発送から発送済みに変更する
def order_not_shipped_to_shipped_view(request, order_id):
    # URLから注文IDを取得し、そのIDに対応するOrderHistoryのインスタンスを取得する
    order_history = get_object_or_404(OrderHistory, id=order_id)
    # 注文履歴の発送済みフラグをtrueに変更する
    order_history.is_shipped = True
    order_history.save()
    return redirect('store:order-not-shipped')

# パスワード再設定用のメール送信ページ
def pass_mail_view(request):
    return render(request, 'store/pass-mail.html')
# 店舗情報設定ページ(閲覧)
def store_info_view(request):
    # print(f"mixin前のuser : {request.__dict__}")
    mixin = MelimitModelMixin()
    mixin.request = request
    user = mixin.get_melimitmodel_user()
    # print(f"店舗情報設定ページのuser : {user.__dict__}")
    # print(f"url : {user.site_url}")
    return render(request, 'store/store-info.html', {'user': user,})

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
        print(f"form : {form}")
        if form.is_valid():
            form.save()
            return render(request, 'store/store-info.html', {'form': form, 'user': user,})
        else:
            print('失敗')
            print(form.errors)
    else:
        print('postじゃないです')
        form = MelimitStoreEditForm(instance=user.melimitstore)
        print(f"form : {form}")
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
@never_cache
#「実際の商品ページを見る」⇒ログアウト⇒ブラウザバックさせないためにnever_cacheを使用
@login_required
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
        # print(product_form.instance.store)
        sale_form.instance.store = user.melimitstore
        # sale_form.instance.storeを表示する
        # print(sale_form.instance.store)
        # ↓forms.pyでself.instance.〇〇を使用するため、instanceを指定する
        sale_form.instance.product = product_form.instance
        threshold_form.instance.sale = sale_form.instance
        # ↑forms.pyでself.instance.〇〇を使用するため、instanceを指定する
        # ここで表示してもdbに保存前なので、表示できない
        print("product_form.instance.product:",sale_form.instance.product.__dict__)
        print("threshold_form.instance.sale:",threshold_form.instance.sale.__dict__)
        
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
        # print(f'Username: {user.username}') # まだ認証前なので、userも存在しない
        # print(f'Username: {form.data.get("username")}') # formにusernameがないので、form.data.get("username")はエラーになる
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
            # userのmodelがMelimitStoreならログイン成功
            if user.__class__.__name__ == 'MelimitStore':
                login(request, user)
                print('ログイン成功')
                return redirect('store:index')
            # elif user.__class__.__name__ != 'MelimitStore':
            #     print('ログイン失敗')
            #     # 店舗側以外のユーザーがログインしようとした場合は、エラーメッセージを表示する
            #     form.add_error(None, '店舗の方以外はログインできません。')  # ユーザーが認証できない場合のエラーメッセージ
            else:
                # フォームが無効な場合の処理をここに書く
                print('pass')
                form.add_error(None, 'メールアドレスまたはパスワードが間違っています。')  # ユーザーが認証できない場合のエラーメッセージ
                # return render(request, 'account/store_login.html', {'form': form})
        else:
            print(form.errors)
            print('rogin-error')
        return render(request, 'account/store_login.html', {'form': form})
    else:
        form = MelimitStoreLoginForm()

        if 'backend' in request.session:
            del request.session['backend']
        request.session['backend'] = 'accounts.backends.MelimitStoreModelBackend'
        print(f'session: {request.session}')
        print(f'session: {dict(request.session)}')

        return render(request, 'account/store_login.html', {'form': form})

# ログイン後の店舗管理画面
# indexを使用している為、未使用
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