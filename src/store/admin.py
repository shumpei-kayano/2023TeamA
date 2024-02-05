from django.contrib import admin
from .models import Product

# Register your models here.
# Productモデルをadminページで編集できるようにする
admin.site.register(Product)