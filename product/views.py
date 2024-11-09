from django.shortcuts import get_object_or_404, render

from product.models import Category, Product, ProductImage


def get_category_data(category_name):
    # İlgili kategoriyi alıyoruz
    category = get_object_or_404(Category, name=category_name, is_active=True)
    all_category = Category.objects.filter(is_active=True)
    # İlgili kategorideki aktif ürünleri alıyoruz
    products = Product.objects.filter(category=category, is_active=True)

    # Tüm aktif kategorileri alıyoruz
    categories = Category.objects.filter(is_active=True)

    return {
        'categories': categories,
        'category': category,
        'products': products,
        'all_category':all_category,
    }



# get_category_data fonksiyonundan gelen category_name değerinine göre ürünler listeleniyor
def product(request, category_name):
    # category_name değerine göre ilgili kategoriyi alıyoruz
    category = get_object_or_404(Category, name=category_name, is_active=True)
    
    # İlgili kategorideki aktif ürünleri alıyoruz
    products = Product.objects.filter(category=category, is_active=True)

    # Tüm aktif kategorileri alıyoruz (sidebar veya filtreleme için kullanabiliriz)
    categories = Category.objects.filter(is_active=True)

    # context olarak verileri şablona gönderiyoruz
    context = {
        'categories': categories,  # Tüm kategoriler
        'category': category,      # Şu an seçili kategori
        'products': products,      # Seçilen kategorinin ürünleri
    }
    
    return render(request, 'base/product_card_and_catergori.html', context)








def product_detail(request, product_pk):
    # Belirtilen product_pk'ye sahip ürünü al
    product = get_object_or_404(Product, pk=product_pk)

    # Ürüne ait resimleri al
    product_images = product.images.all()  # Related name kullanarak

    # get_category_data fonksiyonundan categories değerini alıyoruz
    category_data = get_category_data(product.category.name)
    categories = category_data['categories']

    context = {
        'product': product,
        'product_images': product_images,
        'categories': categories,
    }
    return render(request, 'base/product_detail.html', context)
