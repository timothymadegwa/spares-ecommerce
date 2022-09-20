from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('spares', views.spares, name = 'spares'),
    path('accessories', views.accessories, name = 'accessories'),
    path('update_item', views.update_item, name='update_item'),
    path('inventory/<int:id>', views.inventory, name='inventory'),
    path('orders', views.orders, name='orders'),
    path('order/<int:id>', views.order, name='order'),
]