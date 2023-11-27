from django import forms
from .models import Product, Sale

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        exclude = ['store'] # storeは自動で入るので、フォームには表示しない
        fields = ['product_name', 'product_price', 'weight', 'product_image', 'product_category']
    
    # # ログインしているMelimitStoreのidが自動で入るようにする
    # def save(self, commit=True):
    #     product = super().save(commit=False)
    #     product.store = self.request.user.melimitstore  # ログインユーザーのMelimitStoreインスタンスを設定
    #     if commit:
    #         product.save()
    #         print('product.save()成功')
    #     print('product.save()失敗')
    #     return product


class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        exclude = ['product', 'store']
        fields = ['sale_price', 'sale_start', 'sale_end', 'stock', 'expiration_date', 'description', 'sale_type']