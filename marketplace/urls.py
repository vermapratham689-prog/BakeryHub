from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('shops/', views.shops, name='shops'),
    path('shop/<int:shop_id>/', views.shop_detail, name='shop_detail'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('shop/profile/', views.shop_profile, name='shop_profile'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('orders/<int:order_id>/status/', views.order_status, name='order_status'),
    path('shop/<int:shop_id>/review/', views.add_review, name='add_review'),
    path('marketing/campaigns/', views.campaigns, name='campaigns'),
    path('marketing/campaigns/add/', views.campaign_add, name='campaign_add'),
    path('marketing/analytics/', views.marketing_analytics, name='marketing_analytics'),
    path('offers/add/', views.offer_add, name='offer_add'),
    path('offers/<int:offer_id>/toggle/', views.offer_toggle, name='offer_toggle'),
]
