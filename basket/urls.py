from django.urls import path
from . import views
app_name = 'basket'  # Uygulama adı tanımlandı
urlpatterns = [
    path('', views.basket, name='basket'),  # Ana sepet görünümü
    path('add/<int:product_id>/', views.basket, name='add_to_basket'),  # Ürünü sepete ekleme
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),  # Sepet 
    #path('update-quantity/', views.update_quantity, name='update_quantity'),


    
    path('remove_item/', views.remove_item, name='remove_item'),
    path('cart/items/', views.cart_items, name='cart_items'),
    path('update-quantity/', views.update_quantity, name='update_quantity'),



    
]
