from django.urls import path
from . import views
app_name = 'product' 
urlpatterns = [
    path('<str:category_name>', views.product, name='product'),
    path('product_detail/<int:product_pk>', views.product_detail, name='product_detail'),
    
   
]
