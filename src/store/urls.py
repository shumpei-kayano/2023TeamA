from django.urls import path
from . import views
from .views import ProductAndSaleDeleteView
# accountsアプリviews.pyのStoreCreateViewをインポート
# from accounts.views import StoreCreateView

app_name = 'store'

urlpatterns = [
    # ログイン後の店舗トップページ（グラフとか表示れるところ）
    path('index', views.index, name='index'),
    # 発送済み注文履歴ページ
    path('order-history', views.order_history_view, name='order-history'),
    # 発送済み注文履歴ページの中身
    path('order-history-content/<int:order_id>/', views.order_history_content_view, name='order-history-content'),
    # 未発送注文一覧ページ
    path('order-not-shipped', views.order_not_shipped_view, name='order-not-shipped'),
    # 未発送注文一覧ページの中身
    path('order-not-shipped-content/<int:order_id>/', views.order_not_shipped_content_view, name='order-not-shipped-content'),
    # 未発送から発送済みに変更
    path('order-not-shipped-to-shipped/<int:order_id>/', views.order_not_shipped_to_shipped_view, name='order-not-shipped-to-shipped'),
    # 商品管理一覧ページ
    path('product-manage', views.product_manage_view, name='product-manage'),
    # 商品新規登録ページ
    path('create-general-purchase', views.create_general_purchase_view, name='create-general-purchase'),
    path('create-group-purchase', views.create_group_purchase_view, name='create-group-purchase'),
    # 商品詳細ページ
    path('sale_detail/<int:pk>', views.sale_detail_view, name='sale_detail'),
    # path('detail-general', views.detail_general_view, name='detail-general'),
    # path('detail-group', views.detail_group_view, name='detail-group'),
    # 商品編集ページ
    path('detail-general-edit/<int:product_id>/', views.detail_general_edit_view, name='detail-general-edit'),
    path('detail-group-edit/<int:product_id>/', views.detail_group_edit_view, name='detail-group-edit'),
    # 商品削除
    path('product_delete/<int:pk>', views.product_and_sale_delete_view, name='product_delete'),
    # ログイン処理
    path('store_login/', views.store_login_view, name='store_login'),
    # ログイン後のベースページ
    # path('store_base/', views.store_base_view, name='store_base'),
    # パスワード再設定用のメール送信ページ
    path('pass-mail', views.pass_mail_view, name='pass_mail'),
    # 店舗情報設定ページ
    path('store-info', views.store_info_view, name='store-info'),
    # 店舗情報設定ページの編集
    path('store-info-edit', views.store_info_edit_view, name='store-info-edit'),
    # 店舗の新規登録ページ
    # path('store-create', views.StoreCreateView, name='store-create'),
    # 穴井さんテスト用
    path('test/', views.create_product_and_sale, name='test'), # 商品登録
    path('test2/', views.product_and_sale_list, name='test2'), # 商品一覧
    path('product_and_sale_delete/', ProductAndSaleDeleteView.as_view(), name='product_and_sale_delete'), # 商品複数削除
]
