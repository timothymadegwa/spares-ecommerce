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
    return render(request, 'spares/cart.html')

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
    elif action == "remove":
        cart_item.quantity = cart_item.quantity - 1
    cart_item.save()
    if cart_item.quantity <= 0:
        cart_item.delete()
    return JsonResponse("Item was added", safe=False)

def checkout(request):
    return render(request, 'spares/checkout.html')

def spares(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    context = {
        'inventory' : inventory,
    }
    return render(request, 'spares/spares.html', context)

