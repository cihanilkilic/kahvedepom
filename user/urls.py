
# urls.py
from django.urls import path
from . import views
app_name="user"
urlpatterns = [
    # user account
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    # user address
    path('profil/', views.profil, name='profil'),
    path('addresses/new/', views.address_create, name='address_create'),
    path('delete_address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('change-password/', views.change_password, name='change_password'),
    path('update-name-email/', views.update_name_email, name='update_name_email'),
    # OTURUM AÇMAMIŞ KULLANICLAR İÇİN Şifre sıfırlama URL'leri
    path('password-reset/',  views.password_reset_request, name='password_reset'),
    path('password-reset/confirm/<uidb64>/<token>/',  views.password_reset_confirm, name='password_reset_confirm'),
    # OTURUM AÇMIŞ KULLANICLARIN URL'leri
    path('orders/', views.orders, name='orders'),

]
