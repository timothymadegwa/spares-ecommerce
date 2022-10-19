from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from spares.models import Inventory, Cart
import json

def get_category(request, category_name):
    if request.GET.get('search'):
        search = request.GET.get('search')
        inventory = Inventory.objects.filter(name__icontains=search, category__category_name= category_name) | Inventory.objects.filter(description__icontains=search, category__category_name=category_name)
    else:
        inventory = Inventory.objects.filter(category__category_name=category_name, is_displayed=True, quantity__gt=0)
    if request.user.is_authenticated:
        count = Cart.cart_count(customer_id=request.user.customer.id)
    else:
        count = cookie_cart(request)
        count = count['count']
    p = Paginator(inventory, 30)
    page_num = request.GET.get('page', 1)
    try:
        page = p.page(page_num)
    except PageNotAnInteger:
        page = p.page(1)
    except EmptyPage:
        page = p.page(1)
    context = {
        'inventory' : page,
        'count' : count,
    }
    return context

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