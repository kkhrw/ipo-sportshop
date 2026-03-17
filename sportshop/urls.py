from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),           
    path('about/', views.about, name='about'),   
    path('info/', views.shop_info, name='info'), 
]