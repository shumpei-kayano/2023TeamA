from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('explain/', views.explain_view, name='explain'),
    path('ana_ana/', views.anai, name='ana_ana'),
    path('omae_store_kokoha_useryou/', views.omae_store, name='omae_store'),
    path('omae_user_kokoha_storeyou/', views.omae_user, name='omae_user'),
    path('sinki/', views.sinki, name='sinki'),
    path('what-melimit/', views.what_melimit, name='what_melimit'),
    path('all-products/general/', views.all_products_general, name='all_products_general'),
    path('all-products/joint/', views.all_products_joint, name='all_products_joint'),
    path('contact/', views.contact, name='contact'),
    path('contact/confirm/', views.contact_confirm, name='contact_confirm'),
    path('contact/complete/', views.contact_complete, name='contact_complete'),
    #path('test3/<int:pk>', views.sale_detail_view, name='test3'), # 商品詳細
    path('all-products/general/general-products_detail/<int:pk>', views.general_products_detail, name='general_products_detail'),
    path('all-products/joint/joint-products_detail/<int:pk>', views.joint_products_detail, name='joint_products_detail'),
    path('cart/', views.cart, name='cart'),
    path('notice/', views.notice, name='notice'),
    path('history/', views.history, name='history'),
    path('order_completed/', views.order_completed, name='order_completed'),
    path('favorite/', views.favorite, name='favorite'),
    path('pass_mail/', views.pass_mail, name='pass_mail'),
    path('cash-register/', views.cash_register, name='cash_register'),
    path('signup_choice/', views.signup_choice, name='signup_choice'),
    # テスト用
    # 一覧表示
    path('products/', views.product_list, name='product_list'),
    # 購入数選択
    path('select/<int:product_id>/', views.select_product, name='select_product'),
    # 確認画面
    path('confirm/<int:product_id>/', views.confirm_order, name='confirm_order'),
    # 購入
    path('order/<int:product_id>/', views.order_product, name='order_product'),
    # 購入完了
    path('complete/', views.order_complete, name='order_complete'),
]
