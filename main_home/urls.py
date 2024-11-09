from django.urls import path
from . import views
app_name = 'main_home' 
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search_products, name='search_products'),
    
]
