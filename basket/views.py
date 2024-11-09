from django.http import JsonResponse
from django.shortcuts import redirect, render
from product.models import Category, Product
from product.views import get_category_data
from .models import *
# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt


def basket(request, product_id=None):
    # GET isteği ile sayfa yüklendiğinde sadece kategorileri ve sepet öğelerini al
    if request.method == 'GET':
        cart_items = []

        if request.user.is_authenticated:
            # Kullanıcının sepetindeki öğeleri al
            cart_items = CartItem.objects.filter(user=request.user)

        context = {
            'cart_items': cart_items,
        }
        return render(request, 'basket/basket.html', context)

    # POST isteği ile ürün sepete eklenirken çalışacak kısım
    if request.method == 'POST':
        if not request.user.is_authenticated:
            # Eğer kullanıcı oturum açmamışsa hata mesajı döndür
            return JsonResponse({'message': 'Lütfen oturum açın.'}, status=401)
        
        if product_id:
            product = get_object_or_404(Product, id=product_id)
            product_image = product.images.first()  # İlk resmi al

            # CartItem oluşturma işlemi
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                defaults={
                    'quantity': 1,
                    'total_amount': product.price,
                    'price': product.price,
                    'basket_image': product_image.image if product_image else None
                }
            )
            
            if not created:
                # Eğer ürün zaten sepette varsa, miktarı artır ve toplam tutarı güncelle
                cart_item.quantity += 1
                cart_item.total_amount += cart_item.price
                cart_item.save()

            # Başarı mesajı döndür
            return JsonResponse({'message': 'Ürün sepete eklendi!'})
        else:
            return JsonResponse({'message': 'Ürün bulunamadı.'}, status=404)
    else:
        return JsonResponse({'message': 'Geçersiz istek yöntemi.'}, status=405)












# YENİLERRRRRRRR
from django.contrib.auth.decorators import login_required

@login_required
def cart_items(request):
    # Oturum açmış kullanıcının sepetindeki ürünleri al
    cart_items = CartItem.objects.filter(user=request.user)

    # Sepet bilgilerini JSON formatında döndür
    data = {
        'items': [
            {
                'product_id': item.product.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'total_amount': str(item.total_amount),
                'basket_image': item.basket_image.url if item.basket_image else None
            }
            for item in cart_items
        ]
    }
    return JsonResponse(data)

@csrf_exempt  # CSRF korumasını geçici olarak devre dışı bırak
def update_quantity(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action') 
        quantity = request.POST.get('quantity')

        # Kullanıcı ve ürün bilgilerini al
        cart_item = get_object_or_404(CartItem, product_id=item_id, user=request.user)
        
        # Price değeri boş mu kontrol et
        if cart_item.price is None:
            return JsonResponse({'error': 'Fiyat bilgisi bulunamadı.'}, status=400)

        # Miktarı ve toplam tutarı güncelle
        try:
            quantity = int(quantity)  # Miktarı tamsayıya çevir
            if quantity < 1:
                return JsonResponse({'error': 'Miktar 1\'den az olamaz.'}, status=400)

            cart_item.quantity = quantity
            cart_item.total_amount = cart_item.price * cart_item.quantity  # Toplam fiyatı güncelle
            cart_item.save()

            # Toplam fiyatı hesapla
            total_price = sum(item.total_amount for item in CartItem.objects.filter(user=request.user))

            return JsonResponse({
                'quantity': cart_item.quantity,  # Yeni miktar
                'total_price': cart_item.total_amount,  # Yeni ürün toplamı
                'total_money': total_price  # Genel toplam
            })
        except ValueError:
            return JsonResponse({'error': 'Geçersiz miktar.'}, status=400)

    return JsonResponse({'error': 'Geçersiz istek.'}, status=400)




def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        # Kullanıcının sepetindeki tüm öğeleri al
        cart_items = CartItem.objects.filter(user=request.user)

        # Toplam ürün sayısını hesapla
        total_product_count = sum(item.quantity for item in cart_items)  # Her öğedeki miktarları topla
        
        return JsonResponse({"cart_count": total_product_count})  # Toplam ürün sayısını döndür

    return JsonResponse({"cart_count": cart_count})  # Oturum açmamışsa 0 döner




def remove_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')

        # Kullanıcının sepetindeki ürünü bul ve sil
        try:
            item = get_object_or_404(CartItem, product_id=item_id, user=request.user)
            item.delete()

            # Kalan toplam ücreti hesaplayın
            total_money = sum([i.quantity * i.product.price for i in CartItem.objects.filter(user=request.user)])

            return JsonResponse({
                'message': 'Ürün sepetten kaldırıldı',
                'total_money': total_money
            })
        except CartItem.DoesNotExist:
            return JsonResponse({'error': 'Ürün bulunamadı'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)  # Hata mesajı döndür

    return JsonResponse({'error': 'Invalid request'}, status=400)