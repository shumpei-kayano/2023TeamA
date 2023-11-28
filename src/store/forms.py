from django import forms
from .models import Product, Sale

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['store'] # storeは自動で入るので、フォームには表示しない
        fields = ['product_name', 'product_price', 'weight', 'product_image', 'product_category']
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'input-active', 
                'placeholder': '商品名を入力してください', 
                'required': 'required'
            }),
            'product_category': forms.Select(attrs={
                'class': 'input-active'
            }),
            'weight': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '重量をg（グラム）で入力してください（※半角数字）', 
                'required': 'required'
            }),
            'product_image': forms.ClearableFileInput(attrs={
                'class': 'input-active', 
                'placeholder': '画像を選択してください',
                'required': 'required',
                'multiple': True,
                'accept': 'image/*'
            }),
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['product', 'store']
        fields = ['sale_price', 'sale_start', 'sale_end', 'stock', 'expiration_date', 'description', 'sale_type']
        widgets = {
            'sale_price': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '販売価格を入力してください（※半角数字）', 
                'required': 'required'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '在庫数を入力してください（※半角数字）', 
                'required': 'required'
            }),
            'expiration_date': forms.DateInput(attrs={
                'class': 'input-active', 
                'placeholder': '賞味期限を入力してください',
                'required': 'required',
                'type': 'date'
            }),
            'description': forms.Textarea(attrs={
                'class': 'input-active', 
                'placeholder': '商品説明を入力してください',
                'required': 'required'
            }),
        }