from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from accounts.forms import MelimitStoreLoginForm
from accounts.models import MelimitStore, MelimitUser
from accounts.mixins import MelimitModelMixin
from store.models import Sale, Product,ThresholdCheck
import random
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# orderhistoryをimportする
from .models import OrderHistory
# Create your views here.
# @login_required
def index(request):
    print(request.user)
    # ログインしているか
    if request.user.is_authenticated:
        # ログインしているのがユーザーか
        if request.user.user_type == 'melimit_user' :
            user_id = request.user.id
            # user_id = request.session.get(''user_id')
            print(f'user_id: {user_id}')
            #MelimitUserオブジェクトにtasteが入っている
            user = MelimitUser.objects.get(id=user_id)
            print(f'user: {user}')
            user_taste = user.taste  # ユーザーの好みを取得
            print(user_taste)
            matching_sales = Sale.objects.filter(product__product_category=user_taste).order_by('?')[:3]  # ユーザーの好みに合った商品をランダムに3つ取得
            print('mat:',matching_sales)
            for i in matching_sales:
                print('i.pk:',i.pk)
            
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
        #全商品のうちランダムに三つ取得 allだと使用ごとに中身が変わるのでfilter
        #printが呼び出されるたびにランダムが実施されるのでリストにすることでsalesの時点で固定化する
        #sales_randomsにはオブジェクトが３つ入る
        sales_randoms = list(Sale.objects.filter().order_by('?')[:3])
        print('1', sales_randoms)
        print('2', sales_randoms)
        #type = melのときに閾値を取得する　複数の時にどのように取得するか　共同一覧の時は専用の引数に必要な情報をすべて入れた 一般はそのまま取得できる
        #一般と共同の情報が混ざっているときの取得方法
        #salesの中身を新しい変数に入れていく　
        #一般ならそのまま格納
        #共同なら閾値、閾値チェックの情報を取得しまとめる（共同一覧と同じ方法)
        # 全体を入れる
        sales_random = []
        #閾値を取り出すため
        thresholds = {}
        # iはsaleオブジェクト
        for i in sales_randoms:
            if i.sale_type == 'general_sales':
                print('general_salesです')
                #一般の必要な情報、名前、画像、割引率、販売額
                sale = {
                    'name':i.product.product_name,
                    'image':i.product.product_image,
                    'discount_rate':i.discount_rate(),
                    'sale_price':i.sale_price,
                }
                sales_random.append(sale)
            else:
                print('melimit_salesです') 
                #商品の閾値を取得し引数をpkにして変数に格納
                thresholds[i.pk] = list(i.threshold_set.all())
                print(thresholds[sale.pk])
                #商品にある閾値すべてが出るのでforループ 閾値が一つなので問題ない
                for u in thresholds[sale.pk]:
                    print(u.threshold)
                    print(i.sale_price)
                    print(u.discount_rate)
                    #discount_amount 割引額
                    print(u.discount_amount())
                    #割引額を計算する
                    discounted_amount = u.discount_amount
                    #割引後の値段を計算
                    discounted_price = round(sale.sale_price * (100 - u.discount_rate) / 100)
                #共同の必要な情報、名前、画像、閾値の割引率、販売額、閾値クリア後の値段、閾値クリアに必要な個数、現在の個数
                    sale = {
                        'name':,
                        'image':,
                        'th_discount_rate':,
                        'sale_price':,
                        'discounted_price':,
                        'threshold':,
                        'count':,
                    }
                    sales_random.append(sale)
        #閾値を出す 閾値が一つなのでループは一回
                
            
                            #商品情報と閾値情報、割引後の値段等を一括りにするsale_infos
                # for sale in sales:
                #     print(sale)
                #     print(sale.threshold_set.all())
                #     thresholds[sale.pk] = list(sale.threshold_set.all())
                #     print(thresholds[sale.pk])
                    #閾値を出す 閾値が一つなのでループは一回
                    # for i in thresholds[sale.pk]:
                        
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
            discounted_price = round(sale.sale_price * (100 - i.discount_rate) / 100)
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
    #閾値の現在の個数を取得する
    # check = ThresholdCheck(sale=sale,user=user,threshold=i,count=quantitys)
    return render(request, 'user/joint-products_detail.html', {'sale': sale,'sale_infos':sale_infos,'related_sales':related_sales})

# カート
#セッションからカートを取得し、詳細情報をデータベースから取得する
def cart(request):
    #request.session['cart']が存在するかどうかのif
    if 'cart' not in request.session:
        return render(request, 'user/cart.html')
    else:
        cart = request.session['cart']
        print('cart',cart)
        cart_items = []
        all_price = 0
        #カートの各商品ごとにidと数量をループ
        for pk, quantity in cart.items():
            sale = get_object_or_404(Sale, id=pk)
            #sale.pk商品の主キー(プライマリーキー)
            print('sale.pk:',sale.pk)
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
        all_price_100 = all_price + 100
    return render(request, 'user/cart.html', {'cart_items': cart_items,'all_price':all_price,'all_price_100':all_price_100})
    # return render(request, 'user/cart.html')

#お知らせ詳細
def notice_detail(request):
    return render(request, 'user/notice-detail.html')

# 注文詳細
def history(request):
    #注文履歴からデータを取得　ログインしているユーザーのpkと注文履歴のuserを比較し同じものを取得
    #商品名
    #商品画像
    #カテゴリー
    #商品の価格
    #数量
    #小計
    #注文日時
    #発送状況
    user_id = request.user.id
            # user_id = request.session.get('user_id')
    print(f'user_id: {user_id}')
            #MelimitUserオブジェクトにtasteが入っている
    users = MelimitUser.objects.get(id=user_id)
    print('users:',users)
    order_history = OrderHistory.objects.filter(orderhistory_user=users)
    for i in order_history:
        print('order:',i,vars(i))
    return render(request, 'user/history.html',{'users':users,'order_history':order_history})
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
    if request.user.is_authenticated:
        user_id = request.user.id
            # user_id = request.session.get('user_id')
        print(f'user_id: {user_id}')
            #MelimitUserオブジェクトにtasteが入っている
        user = MelimitUser.objects.get(id=user_id)
        #氏名 電話番号 住所 情報 郵便番号 都道府県 市区町村 番地 建物名
    #ログインしていなかったらログインするように促す
    #ログインしていたら下の処理をする
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
        #cart_itemsはカートの全商品
        print(cart_items)
        cart_item_gen = []
        cart_item_mel = []
        for i in cart_items:
            print(i['sale_type'])
            if i['sale_type'] == '一般商品':
                cart_item_gen.append(i)
            else:
                cart_item_mel.append(i)
        print('一般商品',cart_item_gen)
        print('共同商品',cart_item_mel)
        # sale_typeごとに分ける？
        total_gen = 0
        total_gen = sum(item['total_price'] for item in cart_item_gen)
        total_gen_100 = sum(item['total_price'] for item in cart_item_gen) + 100
        total_mel = 0
        total_mel = sum(item['total_price'] for item in cart_item_mel)
        total_mel_100 = sum(item['total_price'] for item in cart_item_mel) + 100
        #total_gen が空の場合
        all_total = 0
        
        if total_gen == 0:
            print(1)
            all_total = total_mel_100
        #total_melが空の場合
        elif total_mel == 0:
            print(2)
            all_total = total_gen_100
        else:
            print(3)
            all_total = total_gen_100 + total_mel_100 - 100
        print(all_total)
        print(request.session)
        #sessionの中身を全部表示
        print(request.session['cart'].items())
        
        return render(request, 'user/cash-register.html',{'cart_items':cart_items,'cart_item_gen':cart_item_gen,'cart_item_mel':cart_item_mel,'total_gen':total_gen,'total_mel':total_mel,'total_gen_100':total_gen_100,'total_mel_100':total_mel_100,'user':user,'all_total':all_total})
    else:
        return render(request,)
#新規登録
def signup_choice(request):
    return render(request, 'user/signup-choice.html')

def add_to_cart(request, pk):
    sale = get_object_or_404(Sale, id=pk)
    #カート全体
    # cart = request.session['cart']
    #カート全体から商品すべてをループして該当のpkがあるか探す
    
    cart = request.session.get('cart', {})
    quantity = int(request.POST.get('quantity'))
    print('cart:',cart.items())
    #該当するpkなら個数を追加して更新 違うとき？ cart[pk]が空の時であって、cart[pk]が存在していないといけない
    for item_pk, quantitys in cart.items():
        print('item_pk',item_pk)
        print(type(pk))
        print('pk',pk)
        print(type(item_pk))
        if pk == int(item_pk):
            pk = str(pk)
            print('更新前cart[pk]',cart[pk])
            cart[pk] += quantity
            print('更新後cart[pk]:',cart[pk])
            break
    #item_pkだとfor外なのでlocal引数を使うなと言われる
    pk = str(pk)
    print('cart:add',cart)
    if not pk in cart:
        cart[pk] = quantity
        print('cart[pk]:',cart[pk])
    request.session['cart'] = cart
    # if pk in cart:
    #     print('cart[pk]',cart.pk)
    #     cart[pk] += quantity
    # else:
        
    #     cart[pk] = quantity
    #     print('cart[pk]',cart[pk])
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

# テスト/商品一覧表示
def product_list(request):
    print('テスト/商品一覧表示のビュー')
    products = Product.objects.all()
    sales = Sale.objects.all()
    return render(request, 'user/01_itiran_test.html', {'products': products, 'sales': sales,})

# テスト/商品選択
def select_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # productインスタンスからSaleインスタンスを取得
    sale = Sale.objects.get(product_id=product.id)
    return render(request, 'user/02_tyuumonn_test.html', {'product': product, 'sale': sale})

# テスト/注文確認
def confirm_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = request.POST.get('quantity')
    total = product.product_price * int(quantity)
    store = product.store  # ProductモデルからMelimitStoreモデルのインスタンスを取得
    sale = Sale.objects.get(product_id=product.id)  # Saleモデルのインスタンスを取得
    quantity = int(request.POST.get('quantity'))  # 送信された数量を取得
    # amount = product.product_price * quantity  # 合計金額を計算
    co2 = product.weight * 0.4 * quantity  # 合計重量を計算
    # コンテキストに必要なデータを格納
    context = {
        'product': product,
        'quantity': quantity,
        'total': total,
        'store': store,
        'sale': sale,
        'co2': co2,
    }
    return render(request, 'user/03_kakuninn_test.html', context)

# テスト/購入
def order_product(request):
    print('テスト/購入のビュー')
    cart = request.session['cart']
    # cart_items = []
    buy_mels = []
    for pk, quantitys in cart.items():
        print(type(pk))
        # sale = get_object_or_404(Sale, id=pk)
        product = get_object_or_404(Product, id=pk)
        # if request.method == 'POST':
        sale = Sale.objects.get(product_id=pk)
        if sale.sale_type == 'general_sales':
            user = MelimitUser.objects.get(customuser_ptr_id=request.user.id)
            store = product.store  # ProductモデルからMelimitStoreモデルのインスタンスを取得
            sale = Sale.objects.get(product_id=product.id)  # Saleモデルのインスタンスを取得
                # quantity = int(request.POST.get('quantity'))  # 送信された数量を取得
            quantity = quantitys
            amount = sale.sale_price * quantity
            weight = product.weight * quantity 
            order = OrderHistory(sale=sale, product=product, orderhistory_store=store,orderhistory_user=user, amount=amount, quantity=quantity,)
            order.save()
            # del cart[pk]
            #商品ごとにorder.saveを行う
            #リダイレクト先について聞く　必要な情報、タイミング、order_completeと02の違い
            # return redirect('user:order_complete')
        elif sale.sale_type == 'melimit_sales':
            user = MelimitUser.objects.get(customuser_ptr_id=request.user.id)
            store = product.store
            sale = Sale.objects.get(product_id=product.id)
            thresholds = {}
            #index out of range error発生
            thresholds[sale.pk] = list(sale.threshold_set.all())
            print('melの閾値:',thresholds[sale.pk])
            #閾値を出す 閾値が一つなのでループは一回
            for i in thresholds[sale.pk]:
                print('mel:',i.threshold)
                check = ThresholdCheck(sale=sale,user=user,threshold=i,count=quantitys)
                check.save()
                # th,th_ob = check.thresholds()
                # print(th)
                print('check後',check.thresholds()[0])
                if check.thresholds()[0] != None:
                    print('閾値をクリアしました')
                    #閾値をクリアした同じ商品の商品チェックのレコード数分forループ
                    for i in check.thresholds()[1]:
                        print('i:',i)
                        amount = check.thresholds()[0]
                        print(amount)
                        #check.thresholdsからsale,product,store,user,amount,quantitysを取り出す
                        sale = i.sale
                        product = i.sale.product
                        store =i.sale.store
                        user = i.user
                        # amount =
                        quantitys = i.count
                    #この状態だとクリアした商品が来るたびに注文履歴に行く、同じ履歴が何度も並ぶことになる
                        # order = OrderHistory(sale=sale, product=product, orderhistory_store=store,orderhistory_user=user, amount=amount, quantity=quantitys,)
                        # order.save()
                        existing_order = OrderHistory.objects.filter(sale=sale, product=product, orderhistory_store=store, orderhistory_user=user, amount=amount, quantity=quantitys).first()
                        # すでに存在するレコードがない場合のみ、新しいレコードを作成
                        if not existing_order:
                            order = OrderHistory(sale=sale, product=product, orderhistory_store=store, orderhistory_user=user, amount=amount, quantity=quantitys,)
                            order.save()
                else:
                    print('Noneだよ')
            buy_mel = {
                'pk':pk,
                'quantity': quantitys,
            }
            #共同だけを入れるセッションを作成する
            buy_mels.append(buy_mel)
    request.session['mel'] = buy_mels
    print('melのセッション',request.session['mel'])
    #カートの商品のループが終わったらreturn
    #セッションの共同に共同商品を入れる
    #カートの商品が入っているセッションを消す
    del request.session['cart']
    return render(request, 'user/order-completed.html')
    # return render(request, 'user/02_tyuumonn_test.html', {'product': product})
    # return render(request, 'user/order-completed.html')
# テスト/完了画面
def order_complete(request):
    return render(request, 'user/04_complete_test.html')

