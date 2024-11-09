from django.db import models

class Category(models.Model):
    # Kategorinin adı
    name = models.CharField(max_length=255)
    
    # Kategorinin açıklaması
    description = models.TextField(blank=True, null=True)
    
    # Kategorinin üst kategorisi (isteğe bağlı olarak bir alt kategori oluşturmak için)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    
    # Kategoriye ait resim (örneğin, kategori görseli)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    
    # Kategorinin sırası (ürünlerin veya kategorilerin listelenme sırasını belirlemek için)
    order = models.PositiveIntegerField(default=0)
    
    # Kategori eklenme tarihi
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Kategori güncellenme tarihi
    updated_at = models.DateTimeField(auto_now=True)
    
    # Kategorinin aktif olup olmadığını belirten durum
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name




class Product(models.Model):
    # Ürünün adı
    name = models.CharField(max_length=255)
    
    # Ürünün açıklaması
    description = models.TextField(null=True,blank=True)
    description_1 = models.TextField(null=True,blank=True)
    description_2 = models.TextField(null=True,blank=True)
    description_3 = models.TextField(null=True,blank=True)
    description_4 = models.TextField(null=True,blank=True)
    description_5 = models.TextField(null=True,blank=True)
    description_6 = models.TextField(null=True,blank=True)
    
    # Ürünün fiyatı
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Ürün stoğu
    stock = models.PositiveIntegerField(default=0)
    
    # Ürünün kategorisi (farklı bir model ile ilişkilendirilebilir)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Ürün eklenme tarihi
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ürün güncellenme tarihi
    updated_at = models.DateTimeField(auto_now=True)
    
    # Ürünün aktif olup olmadığını belirten durum
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.category ,self.name}"


class ProductImage(models.Model):
    # Resim hangi ürüne ait olduğunu belirtir
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    
    # Resim dosyası
    image = models.ImageField(upload_to='product_images/')
    
    # Resim eklenme tarihi
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - Image {self.pk}"
