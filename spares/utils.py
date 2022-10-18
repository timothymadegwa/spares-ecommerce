import imp
from spares.models import Inventory
import json


def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    cart_items = []
    num_of_items = 0
    for i in cart:
        product = Inventory.objects.get(id = i)
        total = (product.price * cart[i]['quantity'])
        cart_item = {
            'item':{
                'id' : product.id,
                'name': product.name,
                'price' : product.price,
                'photo' : product.photo,
                'discount' : product.discount,
                'selling_price' : product.selling_price,
            },
            'quantity' : cart[i]['quantity'],
            'item_total': total
        }
        cart_items.append(cart_item)
        num_of_items += cart[i]['quantity']

    context = {"count" : num_of_items,
                "inventory" : cart_items
                }
    return context