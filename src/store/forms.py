from django import forms
from .models import Product, Sale

class ProductForm(forms.ModelForm):
    # product_name = forms.CharField(
    #     widget=forms.TextInput(attrs={
    #         'class': 'input-active',
    #         'placeholder': '商品名を入力してください',
    #         'required': 'required'
    #     })
    # )
    # product_category = forms.ChoiceField(
    #     choices=Product.TASTE_CHOICES,
    #     widget=forms.Select(attrs={'class': 'input-active'})
    # )

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
        }

class SaleForm(forms.ModelForm):
    # sale_price = forms.DecimalField(
    #     widget=forms.NumberInput(attrs={
    #         'class': 'input-active',
    #         'placeholder': '販売価格を入力してください（※半角数字）',
    #         'required': 'required'
    #     })
    # )
    class Meta:
        model = Sale
        exclude = ['product', 'store']
        fields = ['sale_price', 'sale_start', 'sale_end', 'stock', 'expiration_date', 'description', 'sale_type']
        widget = {
            'sale_price': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '販売価格を入力してください（※半角数字）', 
                'required': 'required'
            })
        }