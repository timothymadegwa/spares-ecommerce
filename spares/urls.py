from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('cart', views.cart, name = 'cart'),
    path('checkout', views.checkout, name = 'checkout'),
    path('shop/<int:id>', views.shop, name='shop'),
    path('deals', views.deals, name = 'deals'),
    path('update_item', views.update_item, name='update_item'),
    path('inventory/<int:id>', views.inventory, name='inventory'),
    path('orders', views.orders, name='orders'),
    path('order/<int:id>', views.order, name='order'),
]