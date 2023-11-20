from django.shortcuts import render

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