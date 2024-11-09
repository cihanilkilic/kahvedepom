from django.urls import path
from payment_process import views
app_name = 'payment_process' 
urlpatterns = [
    path('payment_view/', views.payment_view, name='payment_view'),
]
