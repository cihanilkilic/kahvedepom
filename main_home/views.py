from django.http import JsonResponse
from django.shortcuts import render
from product.models import *
from django.db.models.functions import Lower
from django.db.models import Q

def index(request):
    if request.method == "GET":
        # Tüm aktif kategorileri al
        categories = Category.objects.filter(is_active=True).values('name')  # Yalnızca adları alır
        # Aktif ürünleri al
        products = Product.objects.filter(is_active=True)
        # İlk 5 ürüne ait resimleri al
        product_images = ProductImage.objects.all()[:5]
        
        # Eğer AJAX isteği ise JSON formatında kategorileri döndür
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            category_names = list(categories)  # QuerySet'i listeye çevir
            return JsonResponse({'categories': category_names})
        else:
            # Normal GET isteğinde HTML döndür
            return render(request, 'main_home/index.html')
        

def normalize_string(s):
    # Türkçe karakterleri normalleştiren fonksiyon
    replacements = {
        'ı': 'i', 'İ': 'i',
        'ğ': 'g', 'Ğ': 'g',
        'ş': 's', 'Ş': 's',
        'ç': 'c', 'Ç': 'c',
        'ö': 'o', 'Ö': 'o',
        'ü': 'u', 'Ü': 'u'
    }
    for search, replace in replacements.items():
        s = s.replace(search, replace)
    return s

def search_products(request):
    query = request.GET.get('q', '').strip()
    product_list = []

    if query:
        # Normalizasyon
        normalized_query = normalize_string(query.lower())

        products = Product.objects.all().annotate(lower_name=Lower('name'))

        product_list = [
            {
                'id': product.id,
                'name': product.name,
                'price': str(product.price),
                'category': product.category.name if product.category else 'Belirtilmemiş',
                'image_url': product.images.first().image.url if product.images.exists() else ''
            }
            for product in products
            if normalized_query in normalize_string(product.lower_name)  # Normalizasyon
        ]

    return JsonResponse({'products': product_list}, json_dumps_params={'ensure_ascii': False})