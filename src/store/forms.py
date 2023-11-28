from django import forms
from .models import Product, Sale

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ['store'] # storeは自動で入るので、フォームには表示しない
        fields = ['product_name', 'product_price', 'weight', 'product_image', 'product_category']

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['product', 'store']
        fields = ['sale_price', 'sale_start', 'sale_end', 'stock', 'expiration_date', 'description', 'sale_type']