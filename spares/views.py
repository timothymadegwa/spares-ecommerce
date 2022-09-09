from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import *

# Create your views here.

# @login_required(login_url='login')
def home(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    context = {
        'inventory' : inventory,
    }
    return render(request, 'spares/home.html', context)

def cart(request):
    cart_items = Cart.objects.filter(user = request.user, is_ordered = False)
    context = {
        "inventory" : cart_items,
        "count" : len(cart_items)
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
    return render(request, 'spares/checkout.html')

def spares(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    context = {
        'inventory' : inventory,
    }
    return render(request, 'spares/spares.html', context)

