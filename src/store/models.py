from django.db import models

class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.IntegerField()
    product_image = models.ImageField(upload_to='images')
    
    #weightに0.4をかける関数
    def CO2(self):
        return str(self.weight * 0.4) + 'kg'
    
    def __str__(self):
        return self.product_name
# Create your models here.


