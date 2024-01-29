from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm
from accounts.models import MelimitStore, MelimitUser
from accounts.mixins import MelimitModelMixin
from store.models import Sale, Product
import random
from django.db.models import Q
from django.http import JsonResponse
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
            #MelimitUserオブジェクトにtasteが入っている
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
    sales_by_choices = {}
    for choice, _ in Sale.SALE_CHOICES:
        sales_by_choices[choice] = Sale.objects.filter(sale_type=choice)
        #sales melimit商品すべて 辞書でkeyを指定し、valueを取り出す
    sales = sales_by_choices['melimit_sales']
    #for文の最後のみ入っている すべてが入るように
    #thresholdsを辞書のままテンプレートに送るとめんどくさいのでリスト型にしたい
    thresholds = {}
    #商品情報と閾値情報、割引後の値段等を一括りにするsale_infos
    sale_infos = []
    for sale in sales:
        print(sale)
        print(sale.threshold_set.all())
        thresholds[sale.pk] = list(sale.threshold_set.all())
        print(thresholds[sale.pk])
        #閾値を出す 閾値が一つなのでループは一回
        for i in thresholds[sale.pk]:
            print(i.threshold)
            print(sale.sale_price)
            print(i.discount_rate)
            #discount_amount 割引額
            print(i.discount_amount())
            #割引額を計算する
            discounted_amount = i.discount_amount
            #割引後の値段を計算
            discounted_price = sale.sale_price *(100-i.discount_rate)/100
            sale_info = {
                'sale_pk':sale.pk,
                'product_name':sale.product.product_name,
                'product_price':sale.product.product_price,
                'weight':sale.product.weight,
                'product_image':sale.product.product_image,
                'product_category':sale.product.product_category,
                'sale_price':sale.sale_price,
                'sale_start':sale.sale_start,
                'sale_end':sale.sale_end,
                'stock':sale.stock,
                'expiration_date':sale.expiration_date,
                'description':sale.description,
                'sale_type':sale.sale_type,
                'discount_rate':i.discount_rate,
                'threshold':i.threshold,
                'discounted_amount':discounted_amount,
                'discounted_price':discounted_price,
                'store_image':sale.product.store.store_image,
                'site_url':sale.product.store.site_url,
                'email':sale.product.store.email,
                'store_name':sale.product.store.username,
                'postal_code':sale.product.store.postal_code,
                'prefecture':sale.product.store.prefecture,
                'city':sale.product.store.city,
                'address':sale.product.store.address,
                'phone_number':sale.product.store.phone_number,
            }
        sale_infos.append(sale_info)
        # ここでthresholdsを使用する
        #salesをひとつずつsaleに入れて、saleごとに閾値は一つなのでsalesをfor文で回すときに同時に閾値もfor文を回すとその商品の閾値が取得できる。が、閾値が複数の時や、対応場所がずれた時に対応できない
    print(2)
    #この段階で辞書型 商品は閾値を持っていないので辞書型で関連性を持たせる必要がある
    print(thresholds)
    for i,j in thresholds.items():
        print('-----')
        print(i)
        print(j)
        for u in j:
            print(u.threshold)
        print('-----')
    #sale_pkは引数でしかない thresholdsの一つ目から順番に出しているだけ
    for sale_pk in thresholds:
        #sale_pkにintが入った
        print(sale_pk)
        #辞書型のkeyとしてsale_pkを使用し、valueを取得する
        for threshold in thresholds[sale_pk]:
            print(threshold)
            print(threshold.threshold)
    #しきい値を取得できた thresholdの一つ目の引数=sale.pkのthreshold.threshold
    
    return render(request, 'user/joint-products.html', {'sales': sales, 'thresholds':thresholds, 'sale_infos':sale_infos})

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
    print(sale.product.product_name)
    print(sale.stock)
    print(sale.product.store)
    print(sale.product.store.site_url)
    print(sale.product.store.store_image)
    print(sale.product.store.email)
    print(sale.product.product_category)
    #商品と同じ店舗の商品と、同じカテゴリーの商品を取得する
    # sales = Sale.objects.filter(Q(sale_type='general_sales')| Q(sale_price__gt=1000))
    # related_sales = Sale.objects.filter(Q(product__store=sale.product.store) | Q(product__category=sale.product.product_category))
    # related_sales = Sale.objects.filter(Q(product__store=sale.product.store) | Q(product__product_category=sale.product.product_category)).order_by('?')[:3]
    related_sales = Sale.objects.filter((Q(product__store=sale.product.store) | Q(product__product_category=sale.product.product_category)) & ~Q(product__product_name=sale.product.product_name)).order_by('?')[:3]
    print(related_sales)
    print(related_sales)
    #関連商品のsale_typeを判断
    sale_infos = []
    #３回ループ
    for related_sale in related_sales:
        print(related_sale.sale_type)
        print(related_sale.pk)
        #このsale_typeにかかるのは0~3件　1は問題ない、0と2,3の時に動くように
        if related_sale.sale_type == 'melimit_sales':
            print(related_sale.threshold_set.all())
            for r in related_sale.threshold_set.all():
                print(r)
                #閾値
                print(r.threshold)
                #割引額を計算する
                discounted_amount = r.discount_amount
                #割引後の値段を計算
                discounted_price = related_sale.sale_price *(100-r.discount_rate)/100
                sale_info = {
                    'threshold':r.threshold,
                    'discounted_amount':discounted_amount,
                    'discounted_price':discounted_price,
                    
                }
            sale_infos.append(sale_info)
            #閾値とクリア後の値段、現在の数
    print(sale.product.product_name)

    return render(request, 'user/general-products_detail.html', {'sale': sale, 'related_sales':related_sales})

# def sale_detail_view(request, pk):
    
#     sale = get_object_or_404(Sale, id=pk)
#     # ログイン中のユーザーだけが商品詳細ページを見れるようにする

#     if user.is_authenticated:
#         try:
#             # saleのpkとmelimitstoreオブジェクトの組み合わせが正しい場合のみDBからsaleを取得する
#             # つまり、urlを直接入力しても他店のsaleは取得できない
#             sale = Sale.objects.get(id=pk, store=user.melimitstore)
#         except ObjectDoesNotExist:
#             print('ログインしているmelimitstoreと取得したいsaleのmelimitstoreが一致しません')
#             return render(request, 'store/test3_error.html')
#         if sale.sale_type == 'general_sales':
#             return render(request, 'store/detail-general.html', {'sale': sale, 'user': user,})

# 共同購入商品詳細
def joint_products_detail(request,pk):
    #id=pkにより、１商品に固定されるはず
    sale = Sale.objects.get(id=pk)
    print(sale)
    print(sale.threshold_set.all())
    thresholds = {}
    #商品情報と閾値情報、割引後の値段等を一括りにするsale_infos
    sale_infos = []
    thresholds[sale.pk] = list(sale.threshold_set.all())
    print(thresholds[sale.pk])
        #閾値を出す 閾値が一つなのでループは一回
    for i in thresholds[sale.pk]:
        print(i.threshold)
        print(sale.sale_price)
        print(i.discount_rate)
        #discount_amount 割引額
        print(i.discount_amount())
        #割引額を計算する
        discounted_amount = i.discount_amount
        #割引後の値段を計算
        discounted_price = sale.sale_price *(100-i.discount_rate)/100
        sale_info = {
            'sale_pk':sale.pk,
            'product_name':sale.product.product_name,
            'product_price':sale.product.product_price,
            'weight':sale.product.weight,
            'product_image':sale.product.product_image,
            'product_category':sale.product.product_category,
            'sale_price':sale.sale_price,
            'sale_start':sale.sale_start,
            'sale_end':sale.sale_end,
            'stock':sale.stock,
            'expiration_date':sale.expiration_date,
            'description':sale.description,
            'sale_type':sale.sale_type,
            'discount_rate':i.discount_rate,
            'threshold':i.threshold,
            'discounted_amount':discounted_amount,
            'discounted_price':discounted_price,
            'store_image':sale.product.store.store_image,
            'site_url':sale.product.store.site_url,
            'email':sale.product.store.email,
            'store_name':sale.product.store.username,
            'postal_code':sale.product.store.postal_code,
            'prefecture':sale.product.store.prefecture,
            'city':sale.product.store.city,
            'address':sale.product.store.address,
            'phone_number':sale.product.store.phone_number,
        }
    sale_infos.append(sale_info)
    #辞書型の一つ目に全部入っている感じ jisyo[0][~]みたいな
    for sale_info in sale_infos:
        print(sale_info)
    print(sale_infos[0]['sale_pk'])
    #sale_infosの関連商品をrelated_saleとする。条件はcategoryが同じ、またはstore_nameが同じ
    # related_sales = Sale.objects.filter(Q(product__store=sale_infos[0]['sale_pk']) | Q(product__product_category=sale_infos[0]['product_category'])).order_by('?')[:3]
    # print(related_sales)
    #sale_infosはオブジェクトではないのでproduct__storeと比較できない
    # related_sales = Sale.objects.filter(Q(product__store=sale.product.store) | Q(product__product_category=sale_infos[0]['product_category'])).order_by('?')[:3]
    related_sales = Sale.objects.filter((Q(product__store=sale.product.store) | Q(product__product_category=sale_infos[0]['product_category'])) & ~Q(product__product_name=sale_infos[0]['product_name'])).order_by('?')[:3]
    print(related_sales)
    #sale.product.storeはオブジェクトが格納されるので文字列と比較しようとしてエラーが発生した。
    #sale_infos[0]['store_name']は文字列なのでint型と比較できない
    #オブジェクトの中身、メソッド、属性の名前を出力できる
    # print(dir(sale.product.store))
    return render(request, 'user/joint-products_detail.html', {'sale': sale,'sale_infos':sale_infos,'related_sales':related_sales})

# カート
#セッションからカートを取得し、詳細情報をデータベースから取得する
def cart(request):
    #request.session['cart']が存在するかどうかのif
    if 'cart' not in request.session:
        return render(request, 'user/cart.html')
    else:
        cart = request.session['cart']
        cart_items = []
        all_price = 0
        #カートの各商品ごとにidと数量をループ
        for pk, quantity in cart.items():
            sale = get_object_or_404(Sale, id=pk)
            #sale.pk商品の主キー(プライマリーキー)
            print(sale.pk)
            if sale.sale_type == 'general_sales':
                sale_type = '一般商品'
            else:
                sale_type = '共同販売商品'
            
            all_price += sale.sale_price * quantity
            #商品の商品名、種別(一般or共同)、一つ当たりの価格、数量、合計価格をリストに追加
            cart_items.append({
                'pk':sale.pk,
                'sale_image': sale.product.product_image,
                'sale': sale.product.product_name,
                'sale_type':sale_type,
                'sale_price':sale.sale_price,
                'quantity': quantity,
                'total_price': sale.sale_price * quantity,
            })

    return render(request, 'user/cart.html', {'cart_items': cart_items,'all_price':all_price})
    # return render(request, 'user/cart.html')

#お知らせ詳細
def notice_detail1(request):
    return render(request, 'user/notice-detail1.html')

def notice_detail2(request):
    return render(request, 'user/notice-detail2.html')

def notice_detail3(request):
    return render(request, 'user/notice-detail3.html')

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

# 注文確認
def cash_register(request):
    cart = request.session['cart']
    cart_items = []
    all_price = 0
    #カートの各商品ごとにidと数量をループ
    for pk, quantity in cart.items():
        sale = get_object_or_404(Sale, id=pk)
        #sale.pk商品の主キー(プライマリーキー)
        print(sale.pk)
        if sale.sale_type == 'general_sales':
            sale_type = '一般商品'
        else:
            sale_type = '共同販売商品'
        
        all_price += sale.sale_price * quantity
        #商品の商品名、種別(一般or共同)、一つ当たりの価格、数量、合計価格をリストに追加
        cart_items.append({
            'pk':sale.pk,
            'sale_image': sale.product.product_image,
            'sale': sale.product.product_name,
            'sale_type':sale_type,
            'sale_price':sale.sale_price,
            'quantity': quantity,
            'total_price': sale.sale_price * quantity,
        })
    return render(request, 'user/cash-register.html',{'cart_items':cart_items})

#新規登録
def signup_choice(request):
    return render(request, 'user/signup-choice.html')

def add_to_cart(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity'))
    if pk in cart:
        cart[pk] += quantity
    else:
        cart[pk] = quantity
    request.session['cart'] = cart
    #引数にproduct_idを渡している
    # return redirect('user:cart', product_id=product_id)
    return redirect('user:cart')

#カートの商品の個数を変更する
def update_cart(request):
    pk = request.POST.get('pk')
    quantity = int(request.POST.get('quantity'))

    cart = request.session.get('cart', {})
    cart[pk] = cart.get(pk, 0) + quantity

    request.session['cart'] = cart

    # 新しいカートのデータを作成
    cart_items = []
    #カートの各商品ごとにidと数量をループ
    for pk, quantity in cart.items():
        sale = get_object_or_404(Sale, id=pk)
        if sale.sale_type == 'general_sales':
            sale_type = '一般商品'
        else:
            sale_type = '共同販売商品'
        #商品の商品名、種別(一般or共同)、一つ当たりの価格、数量、合計価格をリストに追加
        cart_items.append({
            'pk':sale.pk,
            'sale_image': sale.product.product_image.url,
            'sale': sale.product.product_name,
            'sale_type':sale_type,
            'sale_price':sale.sale_price,
            'quantity': quantity,
            'total_price': sale.sale_price * quantity,
        })


    return JsonResponse({'cart_items': cart_items})

#カートから商品を削除する
def delete_cart(request):
    pk = request.POST.get('pk')
    print(pk)
    print(11111)
    cart = request.session.get('cart', {})
    del cart[pk]
    print(cart)
    request.session['cart'] = cart

    # 新しいカートのデータを作成
    cart_items = []
    #カートの各商品ごとにidと数量をループ
    for pk, quantity in cart.items():
        sale = get_object_or_404(Sale, id=pk)
        if sale.sale_type == 'general_sales':
            sale_type = '一般商品'
        else:
            sale_type = '共同販売商品'
        #商品の商品名、種別(一般or共同)、一つ当たりの価格、数量、合計価格をリストに追加
        cart_items.append({
            'pk':sale.pk,
            'sale_image': sale.product.product_image.url,
            'sale': sale.product.product_name,
            'sale_type':sale_type,
            'sale_price':sale.sale_price,
            'quantity': quantity,
            'total_price': sale.sale_price * quantity,
        })


    return JsonResponse({'cart_items': cart_items})
#ご利用ガイド（詳細）
def guide_detail(request):
    return render(request, 'user/guide-detail.html')

#ご利用ガイド
def guide(request):
    return render(request, 'user/guide.html')

# お知らせ一覧
def notice(request):
    return render(request, 'user/notice.html')

# MelimitとSDGs
def sdgs(request):
    return render(request, 'user/sdgs.html')

# カテゴリー別商品一覧
def category_products(request):
    return render(request, 'user/category-products.html')
