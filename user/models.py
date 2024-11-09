from datetime import timezone
from django.db import models
from django.contrib.auth.models import User
import uuid

# KULLANICI ADRES MODELİ
class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses", verbose_name="Adresi Oluşturan Kişi")
    first_name = models.CharField(max_length=50, verbose_name="Adı")  # Zorunlu alan
    last_name = models.CharField(max_length=50, verbose_name="Soyadı")  # Zorunlu alan
    phone = models.CharField(max_length=15, verbose_name="Telefon Numarası")  # Zorunlu alan
    city = models.CharField(max_length=100, verbose_name="İl")  # Zorunlu alan
    district = models.CharField(max_length=100, verbose_name="İlçe")  # Zorunlu alan
    mahalle = models.CharField(max_length=200, verbose_name="Mahalle")# Zorunlu alan
    address_title = models.CharField(max_length=100,verbose_name="Adres Başlığı")# Zorunlu alan
    address = models.TextField(verbose_name="Açık Adres")# Zorunlu alan
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")


    def __str__(self):
        return f"{self.address_title} - {self.user.username}"
    





#KULLANICI DAVET KODU MODELİ
class InviteCode(models.Model):
    created_by = models.ForeignKey(User, related_name="created_invite_codes", on_delete=models.CASCADE,verbose_name="Davet kodunu oluşturan kullanıcı")#Bu, davet kodunu oluşturan kullanıcıyı ifade eder.
    used_by = models.ForeignKey(User, related_name="used_invite_codes", on_delete=models.SET_NULL, null=True, blank=True,verbose_name="Davet kodunu kullanan kullanıcı")#Bu, davet kodunu kullanan kullanıcıyı ifade eder
    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)  # Benzersiz davet kodu
    created_at = models.DateTimeField(auto_now_add=True)  # Davet kodu oluşturulma tarihi
    used_at = models.DateTimeField(null=True, blank=True)  # Davet kodu kullanıldığı zaman
    is_active = models.BooleanField(default=True)  # Davet kodunun aktif olup olmadığı

    def __str__(self):
        return f"{self.code} - Created by {self.created_by.username}"

    def mark_as_used(self, user):
        """Davet kodunu kullanan kullanıcıyı belirle ve aktif durumu pasif yap."""
        self.used_by = user
        self.used_at = timezone.now()
        self.is_active = False
        self.save()










# class TemporaryEmail(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, default=6)  # Varsayılan değer yok
#     email = models.EmailField(null=True, blank=True, default='cihanilkilic@gmail.com')
#     verification_code = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)  # Varsayılan değer ile db_default kaldırıldı
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.email


