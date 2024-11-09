from django.db import models
from django.contrib.auth.models import User

from product.models import Product
# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name="Sepete Ekleyen Kişi",blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,verbose_name="Sepetteki Ürün",related_name="product",blank=True, null=True)
    price =models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Fiyat",blank=True, null=True) # Ürünün fiyatını sepette sakla
    quantity = models.PositiveIntegerField(default=1,verbose_name="Ürün Adeti",blank=True, null=True) # Ürünün adetini arttır / azalt
    total_amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name="Total Fiyat",blank=True, null=True)#Toplam fiyatı artır / arttır 
    basket_image=models.ImageField(upload_to='basket_images/',blank=True, null=True, verbose_name="Ürünün Fotoğrafı")
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    # @property
    # def total_price(self):
    #     return self.quantity * self.product.price