from django.shortcuts import redirect, render
from django.http import JsonResponse
from basket.models import CartItem
from django.contrib.auth.decorators import login_required

from user.models import UserAddress
@login_required
def payment_view(request):
    # Eğer kullanıcı oturum açmamışsa yönlendir
    if not request.user.is_authenticated:
        return redirect('user:login')  # 'login' yerine giriş sayfanızın URL adını yazın

    if request.method == "GET":
        # Kullanıcının sepetindeki ürünleri al
        cart_items = CartItem.objects.filter(user=request.user)

        # Sepet bilgilerini JSON formatında hazırlama
        data = {
            'items': [{
                'id': item.id,
                'product_name': item.product.name,
                'quantity': item.quantity,
                'product_image': item.basket_image.url if item.basket_image else None,
                'total_price': item.total_amount
            } for item in cart_items],
            'total_amount': sum(item.total_amount for item in cart_items),  # Toplam tutar
        }

        # Kullanıcının adres bilgilerini sadece oturum açmışsa al
        if request.user.is_authenticated:
            addresses = UserAddress.objects.filter(user=request.user)
            data['addresses'] = [{
                'id': address.id,
                'first_name': address.first_name,
                'last_name': address.last_name,
                'phone': address.phone,
                'city': address.city,
                'district': address.district,
                'mahalle': address.mahalle,
                'address_title': address.address_title,
                'address': address.address
            } for address in addresses]

        # AJAX isteği olup olmadığını kontrol et
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse(data)  # Sepet ve adres bilgilerini JSON formatında döndür

        # AJAX değilse sayfa olarak döndür
        return render(request, 'payment/payment.html', {'data': data})

    # GET dışında bir yöntemle çağrılırsa hata döndür
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
