from django.urls import path
from . import views
from .views import order_history_view, order_not_shipped_view,product_manage_view,create_general_purchase_view,create_group_purchase_view,detail_general_view,detail_group_view,detail_general_edit_view,detail_group_edit_view

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    # 発送済み注文履歴ページ
    path('order-history', views.order_history_view, name='order-history'),
    # 未発送注文一覧ページ
    path('order-not-shipped', views.order_not_shipped_view, name='order-not-shipped'),
    # 商品管理一覧ページ
    path('product-manage', views.product_manage_view, name='product-manage'),
    # 商品新規登録ページ
    path('create-general-purchase', views.create_general_purchase_view, name='create-general-purchase'),
    path('create-group-purchase', views.create_group_purchase_view, name='create-group-purchase'),
    # 商品詳細ページ
    path('detail-general', views.detail_general_view, name='detail-general'),
    path('detail-group', views.detail_group_view, name='detail-group'),
    # ログイン処理
    path('store_login_success/', views.store_login_view, name='store_login_success'),
    # ログイン後のベースページ
    path('store_base/', views.store_base_view, name='store_base'),
    # 穴井さんテスト用
    path('test/', views.create_product_and_sale, name='test'),
    path('test2/', views.product_and_sale_list, name='test2'),
    # 商品詳細ページ
    path('detail-general', views.detail_general_view, name='detail-general'),
    path('detail-group', views.detail_group_view, name='detail-group'),
    # 商品編集ページ
    path('detail-general-edit', views.detail_general_edit_view, name='detail-general-edit'),
    path('detail-group-edit', views.detail_group_edit_view, name='detail-group-edit')
]
