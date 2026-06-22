from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [

    path('', views.home_page, name='home'),
    path('about/', views.about_page, name='about'),
    path('author/', views.author_page, name='author'),

    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
   
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
  
    path('checkout/', views.checkout, name='checkout'),
 
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.profile_view, name='profile'),
]