from django import forms
from .models import Product, Sale, Threshold
from accounts.models import MelimitStore

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
                'class': 'input-active', 
                'required': 'required'
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
                'multiple': False,
                'accept': 'image/*',
                'label': '画像を変更',
            }
            # clearable_file_input_template=('<input type="file" id="{id}" class="{class}" placeholder="{placeholder}" required multiple accept="{accept}" />''<div class="clearable-file-input-label"></div>'),
            ),
            'product_price': forms.NumberInput(attrs={
                'class': 'input-active', 
                'placeholder': '定価を入力してください（※半角数字）', 
                'required': 'required'
            }),
        }

    # 定価のバリデーション
    def clean_product_price(self):
        product_price = self.cleaned_data.get('product_price')
        if product_price is not None and (product_price < 1 or product_price > 1_000_000):
            # raise forms.ValidationError('定価は1円以上100万円以下で入力して下さい。')
            self.add_error('product_price', '定価は1円以上100万円以下で入力して下さい。')
        return product_price

class SaleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    class Meta:
        model = Sale
        exclude = ['product', 'store', ]
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
            'sale_start': forms.DateInput(attrs={
                'id': 'startDateTime',
                'class': 'input-active', 
                'title': '販売開始日時を入力してください',
                'required': 'required',
                # 'type': 'datetime-local',
                'type': 'date',
            }),
            'sale_end': forms.DateInput(attrs={
                'id': 'endDateTime',
                'class': 'input-active', 
                'title': '販売終了日時を入力してください',
                'required': 'required',
                # 'type': 'datetime-local',
                'type': 'date',
            }),
        }

    # formのclassが違うので、cleanメソッドをオーバーライドしてsale_price(販売価格)とproduct_price(定価)を比較する
    # cleanメソッドは、is_valid()が呼ばれた時に自動的に呼ばれる(詳細は個人notionに記載)
    def clean(self):
        print('関数:clean')
        cleaned_data = super().clean()
        sale_price = cleaned_data.get('sale_price')
        print("3番")
        # ↓product_priceをint型に変更したのでこの記述になった
        print(self.instance.product.product_price)
        product_price = self.instance.product.product_price if self.instance.product else None
        # ↑product_priceをint型に変更したのでこの記述になった

        # okパターン(httpリクエストのpostパラメータからstr型で取得し、int型に変換する))
        # product_price = int(self.request.POST.get('product_price')) if self.request else None

        # okパターン(cleaned_dataからint型で取得する)
        # formを定義後、is_validでバリデーションとクリーニングを行い、formの値を正しい型に更新しcleaned_data辞書からint型で値を取得する
        # pro_form = ProductForm(self.request.POST, instance=self.instance.product)
        # if pro_form.is_valid():
        #     product_price = pro_form.cleaned_data.get('product_price')
        # else:
        #     product_price = None

        # 一応okパターン(DBからint型で取得する。ただし、比較前にDB登録しているため、比較結果がNGでも定価だけが登録されてしまう)
        # pro_form = ProductForm(self.request.POST, instance=self.instance.product)
        # if pro_form.is_valid():
        #     saved_pro=pro_form.save(commit=True)
        # product_price = saved_pro.product_price

        # ngパターン
        # self.instance.productで取得できるのは、編集前のproductの情報(DBに保存されている情報)
        # product_price = self.instance.product.product_price if self.instance.product else None

        print("4番")
        print(f"クリーンsale_price:{sale_price}")
        print(f"クリーンproduct_price:{product_price}")
        # product_priceの型を確認
        print(f"product_priceの型:{type(product_price)}")
        if sale_price and product_price and sale_price > product_price:
            self.add_error('sale_price', '販売価格は商品の定価未満で入力して下さい。')
        # if sale_price is not None and (sale_price < 1 or sale_price > 1_000_000):
        #     self.add_error('sale_price', '販売価格は1円以上100万円以下で入力して下さい。')
        return cleaned_data

    # 販売価格のバリデーション
    def clean_sale_price(self):
        print('関数:clean_sale_price')
        sale_price = self.cleaned_data.get('sale_price')
        print(f"sale_price:{sale_price}")
        if sale_price is not None and (sale_price < 1 or sale_price > 1_000_000):
            # raise forms.ValidationError('販売価格は1円以上100万円以下で入力して下さい。')
            self.add_error('sale_price', '販売価格は1円以上100万円以下で入力して下さい。')
        return sale_price

class ThresholdForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
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

    def clean(self):
        # 既存のバリデーションを実行
        # 既存のバリデーションを実行
        cleaned_data = super().clean()
        threshold = cleaned_data.get('threshold')
        print('threshold:', threshold)
        print("テスト")
        # sale_form = SaleForm(self.request.POST, )
        # sale_stock = sale_form.cleaned_data.get('stock') if sale_form.is_valid() else None
        # print('salestock', sale_stock)
        print(self.instance.sale.stock)
        sale_stock = self.instance.sale.stock if self.instance.sale else None
        # sale_stock = self.instance.sale.stock if self.instance.sale else None
        
        print('sale:', sale_stock)

        # thresholdがsaleのstockより大きい場合はエラー
        if sale_stock and threshold > sale_stock:
            print('しきい値が在庫数を超えています。')
            raise forms.ValidationError({
                'threshold': 'Threshold cannot be greater than the stock of the related sale.'
            })

# 全都道府県をリスト化(copilot依頼)
PREFECTURE_CHOICES = [('','選択してください'),('北海道','北海道'),('青森県','青森県'),('岩手県','岩手県'),('宮城県','宮城県'),('秋田県','秋田県'),('山形県','山形県'),('福島県','福島県'),('茨城県','茨城県'),('栃木県','栃木県'),('群馬県','群馬県'),('埼玉県','埼玉県'),('千葉県','千葉県'),('東京都','東京都'),('神奈川県','神奈川県'),('新潟県','新潟県'),('富山県','富山県'),('石川県','石川県'),('福井県','福井県'),('山梨県','山梨県'),('長野県','長野県'),('岐阜県','岐阜県'),('静岡県','静岡県'),('愛知県','愛知県'),('三重県','三重県'),('滋賀県','滋賀県'),('京都府','京都府'),('大阪府','大阪府'),('兵庫県','兵庫県'),('奈良県','奈良県'),('和歌山県','和歌山県'),('鳥取県','鳥取県'),('島根県','島根県'),('岡山県','岡山県'),('広島県','広島県'),('山口県','山口県'),('徳島県','徳島県'),('香川県','香川県'),('愛媛県','愛媛県'),('高知県','高知県'),('福岡県','福岡県'),('佐賀県','佐賀県'),('長崎県','長崎県'),('熊本県','熊本県'),('大分県','大分県'),('宮崎県','宮崎県'),('鹿児島県','鹿児島県'),('沖縄県','沖縄県')]
class MelimitStoreEditForm(forms.ModelForm):
    class Meta:
        model = MelimitStore
        fields = ['username', 'postal_code', 'prefecture', 'city', 'address', 'phone_number', 'store_image', 'site_url']
        # fields = ['username']
        widgets = {
            'prefecture': forms.Select(choices=PREFECTURE_CHOICES, attrs={
                'class': 'store-input-active',
                'name': 'prefecture',
            }),
        }
    def save(self, commit=True):
        user = super().save(commit=True)
        return user