from django.urls import path
from . import views
from .views import order_history_view, order_not_shipped_view,product_manage_view,create_general_purchase_view,create_group_purchase_view

app_name = 'store'

urlpatterns = [
    path('', views.index, name='index'),
    path('order-history', views.order_history_view, name='order-history'),
    path('order-not-shipped', views.order_not_shipped_view, name='order-not-shipped'),
    path('product-manage', views.product_manage_view, name='product-manage'),
    path('create-general-purchase', views.create_general_purchase_view, name='create-general-purchase'),
    path('create-group-purchase', views.create_group_purchase_view, name='create-group-purchase'),
]
