from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
import json
from .models import *

# Create your views here.

# @login_required(login_url='login')
def home(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    count = Cart.cart_count(user_id=request.user.id)
    context = {
        'inventory' : inventory,
        'count' : count,
    }
    return render(request, 'spares/home.html', context)

def spares(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    count = Cart.cart_count(user_id=request.user.id)
    context = {
        'inventory' : inventory,
        'count' : count,
    }
    return render(request, 'spares/spares.html', context)

def inventory(request, id):
    item = get_object_or_404(Inventory, id=id)
    inventory = Inventory.objects.filter(category=item.category).order_by('?').exclude(id=item.pk)
    count = Cart.cart_count(user_id=request.user.id) 
    context = {
        "item" : item,
        "inventory" : inventory,
        "count" : count,
    }
    return render(request, 'spares/inventory.html', context)

def cart(request):
    cart_items = Cart.objects.filter(user = request.user, is_ordered = False)
    count= Cart.cart_count(user_id=request.user.id)
    context = {
        "inventory" : cart_items,
        "count" : count,
    }
    return render(request, 'spares/cart.html', context)

@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    user = request.user
    product = Inventory.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user,item=product, is_ordered = False)

    if action == "add":
        cart_item.quantity = cart_item.quantity + 1
        cart_item.save()
        message = "Item was added to your cart"
        messages.info(request, message)
        return JsonResponse("Item was added", safe=False)
    if action == "remove":
        cart_item.quantity = cart_item.quantity - 1
        cart_item.save()
        if cart_item.quantity <= 0:
            cart_item.delete()
        return JsonResponse("Item was removed", safe=False)
    if action == "delete":
        cart_item.delete()
        return JsonResponse("Item was deleted", safe=False)

def checkout(request):
    if request.method == "POST":
        pass

    cart_items = Cart.objects.filter(user = request.user, is_ordered = False)
    count = sum(cart_items.values_list('quantity', flat=True))

    context = {
        "inventory" : cart_items,
        "count" : count,
    }
    return render(request, 'spares/checkout.html', context)



