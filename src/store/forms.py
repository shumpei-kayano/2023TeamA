from django import forms
from .models import Product, Sale, Threshold

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
                'id': 'example',
                'class': 'input-active', 
                'placeholder': '画像を選択してください',
                'required': 'required',
                'multiple': True,
                'accept': 'image/*',
            }),
            'product_price': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '定価を入力してください（※半角数字）', 
                'required': 'required'
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
            'sale_start': forms.DateTimeInput(attrs={
                'id': 'startDateTime',
                'class': 'input-active', 
                'title': '販売開始日時を入力してください',
                'required': 'required',
                'type': 'datetime-local'
            }),
            'sale_end': forms.DateTimeInput(attrs={
                'id': 'endDateTime',
                'class': 'input-active', 
                'title': '販売終了日時を入力してください',
                'required': 'required',
                'type': 'datetime-local'
            }),
        }

class ThresholdForm(forms.ModelForm):
    class Meta:
        model = Threshold
        fields = ['discount_rate', 'threshold']
        widgets = {
            'discount_rate': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '共同購入達成時の値引率を入力してください（※半角数字）', 
                'required': 'required'
            }),
            'threshold': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '共同購入達成数量を入力してください（※半角数字）', 
                'required': 'required'
            }),
        }