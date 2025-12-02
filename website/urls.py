# ============================================
# 3. website/urls.py
# ============================================

from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('contact/', views.contact, name='contact'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/content/<str:section>/', views.content_edit, name='content_edit'),
    path('dashboard/products/', views.products_manage, name='products_manage'),
    path('dashboard/product/new/', views.product_edit, name='product_new'),
    path('dashboard/product/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('dashboard/product/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('dashboard/services/', views.services_manage, name='services_manage'),
    path('dashboard/service/new/', views.service_edit, name='service_new'),
    path('dashboard/service/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('dashboard/service/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('dashboard/messages/', views.messages_view, name='messages_view'),
    path('dashboard/message/<int:pk>/', views.message_detail, name='message_detail'),
]


