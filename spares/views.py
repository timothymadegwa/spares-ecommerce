from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from accounts.forms import ShippingForm
from .models import *
from helpers import send_mail

# Create your views here.

# @login_required(login_url='login')
def home(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('?')
    spares = inventory.filter(category__category_name="Spare part").order_by('?')[:3]
    accessories = inventory.filter(category__category_name="Accessory").order_by('?')[:3]
    deals = inventory.filter(has_discount=True).order_by('?')[:3]
    count = Cart.cart_count(user_id=request.user.id)
    context = {
        'spares' : spares,
        'accessories' : accessories,
        'deals' : deals,
        'count' : count,
    }
    return render(request, 'spares/home.html', context)

def spares(request):
    if request.GET.get('search'):
        search = request.GET.get('search')
        inventory = Inventory.objects.filter(name__icontains=search, category__category_name="Spare part") | Inventory.objects.filter(description__icontains=search, category__category_name="Spare part")
    else:
        inventory = Inventory.objects.filter(category__category_name="Spare part", is_displayed=True, quantity__gt=0).order_by('?')
    count = Cart.cart_count(user_id=request.user.id)
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
    return render(request, 'spares/spares.html', context)

def accessories(request):
    if request.GET.get('search'):
        search = request.GET.get('search')
        inventory = Inventory.objects.filter(name__icontains=search, category__category_name="Accessory") | Inventory.objects.filter(description__icontains=search, category__category_name="Accessory")
    else:
        inventory = Inventory.objects.filter(category__category_name="Accessory", is_displayed=True, quantity__gt=0).order_by('?')
    count = Cart.cart_count(user_id=request.user.id)
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
    return render(request, 'spares/spares.html', context)

def inventory(request, id):
    item = get_object_or_404(Inventory, id=id)
    inventory = Inventory.objects.filter(category=item.category).order_by('?').exclude(id=item.pk)[:3]
    count = Cart.cart_count(user_id=request.user.id) 
    context = {
        "item" : item,
        "inventory" : inventory,
        "count" : count,
    }
    return render(request, 'spares/inventory.html', context)

def cart(request):
    cart_items = Cart.objects.filter(user = request.user, is_ordered = False).order_by("-id")
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
        form = ShippingForm(request.POST)
        if form.is_valid():
            shipping_name = form.cleaned_data['shipping_name']
            phone = form.cleaned_data['phone_number']
            region = form.cleaned_data['region']
            location = form.cleaned_data['shipping_location']
        else:
            print(form.errors)
            message = "Please fill in all the fields"
            messages.error(request, message)
            return render(request, 'spares/checkout.html')
        shipping = Shipping(user = request.user, shipping_name = shipping_name, phone_number = phone,
                            region = region, shipping_location = location )
        shipping.save()
        cart_items = Cart.objects.filter(user = request.user, is_ordered = False)
        order = Order(user = request.user, shipping_details = shipping)
        order.save()
        order.items.add(*cart_items)
        order.save()
        cart_items.update(is_ordered= True)
        #send_mail([request.user.email],'Order Completed!', 'Thank you for ordering your spare parts with us. Kindly track your order though our website')
        messages.success(request, "Your order has been placed")
        return render(request, 'spares/success.html')

    cart_items = Cart.objects.filter(user = request.user, is_ordered = False).order_by("-id")
    if cart_items:
        count = sum(cart_items.values_list('quantity', flat=True))

        context = {
            "inventory" : cart_items,
            "count" : count,
        }
        return render(request, 'spares/checkout.html', context)
    messages.error(request, "You cannot view this page!")
    return redirect("home")

def orders(request):
    orders = Order.objects.filter(user = request.user).order_by("-id")
    context = {
        "inventory" : orders
    }
    return render(request, 'spares/orders.html', context)

def order(request, id):
    order = get_object_or_404(Order, id=id)
    context = {
        "orders" : order,
    }
    return render(request, 'spares/order.html', context)


