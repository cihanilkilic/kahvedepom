from django.contrib import admin
from .models import Product, ProductImage , Category
# Product ve ProductImage
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)



# Category
class CategoryAdmin(admin.ModelAdmin):
    # Admin panelinde gösterilecek alanlar
    list_display = ('name', 'parent', 'order', 'is_active', 'created_at', 'updated_at')
    
    # Arama yapılabilecek alanlar
    search_fields = ('name', 'description')
    
    # Filtreleme için kullanılabilecek alanlar
    list_filter = ('is_active', 'created_at', 'parent')
    
    # Kayıt düzenleme sayfasında gösterilecek alanların sırası
    fields = ('name', 'description', 'parent', 'image', 'order', 'is_active')
    
    # Varsayılan sıralama düzeni
    ordering = ('order',)

# Kategori modelini admin paneline ekliyoruz
admin.site.register(Category, CategoryAdmin)
