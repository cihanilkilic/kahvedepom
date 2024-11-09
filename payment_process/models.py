import uuid
from django.db import models
from django.contrib.auth.models import User

from product.models import Product
# Create your models here.


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Beklemede'),
        ('received', 'Sipariş Verildi'),
        ('preparing', 'Sipariş Hazırlanıyor'),
        ('in_shipping', 'Sipariş Kargoda'),
        ('completed', 'Tamamlandı'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name="Sipariş Veren Kişi")
    code = models.CharField(max_length=50,verbose_name="Referans Kodu",blank=True,null=True)
    product = models.ForeignKey(Product,on_delete=models.CASCADE,verbose_name="Ürün",related_name="orders",blank=True,null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Birim Fiyat",blank=True,null=True)
    quantity = models.PositiveIntegerField(default=1,verbose_name="Ürün Adeti",blank=True,null=True)
    total_amount = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Toplam Fiyat",editable=False,blank=True,null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending',verbose_name="Sipariş Durumu")
    order_image = models.ImageField(upload_to='order_images/',blank=True,null=True,verbose_name="Ürün Fotoğrafı")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Oluşturulma Tarihi",blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,verbose_name="Güncellenme Tarihi",blank=True,null=True)

    def save(self, *args, **kwargs):
        # Toplam fiyatı otomatik olarak hesapla
        self.total_amount = self.price * self.quantity
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.product} - {self.total_amount} TL"
