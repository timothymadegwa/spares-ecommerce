from spares.models import Inventory, Cart, Order
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
        total = (product.selling_price * cart[i]['quantity'])
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

def cookie_checkout(request, customer, shipping):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        return False
    for i in cart:
        product = Inventory.objects.get(id = i)
        quantity = cart[i]['quantity']
        cart_item = Cart.objects.create(customer = customer, item = product, quantity = quantity)
        cart_item.save()
    
    cart_items = Cart.objects.filter(customer = customer, is_ordered = False)
    order = Order(customer = customer, shipping_details = shipping)
    order.save()
    order.items.add(*cart_items)
    order.save()
    cart_items.update(is_ordered= True)
    #send_mail([customer.email],'Order Completed!', 'Thank you for ordering your spare parts with us. Kindly track your order though our website')
    return True