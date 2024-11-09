from django.http import JsonResponse
from django.shortcuts import render
from product.models import *
from django.db.models.functions import Lower
from django.db.models import Q

def index(request):
    if request.method == "GET":
        categories = Category.objects.filter(is_active=True)
        products = Product.objects.filter(is_active=True)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            category_data = []
            for category in categories:
                category_products = products.filter(category=category)
                product_list = []
                for product in category_products:
                    product_images = ProductImage.objects.filter(product=product)
                    image_url = product_images.first().image.url if product_images.exists() else 'https://via.placeholder.com/250'

                    product_list.append({
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'image_url': image_url,
                    })

                category_data.append({
                    'name': category.name,
                    'products': product_list,
                })
            
            return JsonResponse({'categories': category_data})
        else:
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