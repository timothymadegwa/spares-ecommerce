from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
from django.contrib import messages
import json
from .forms import ShippingForm
from .models import *
from helpers import send_mail
from .utils import cookie_cart, cookie_checkout

# Create your views here.

def home(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('?')
    spares = inventory.filter(category__category_name="Spare parts").order_by('?')[:4]
    accessories = inventory.filter(category__category_name="Accessories").order_by('?')[:4]
    tyres = inventory.filter(category__category_name="Tyres").order_by('?')[:4]
    deals = inventory.filter(has_discount=True).order_by('?')[:4]
    categories = Category.objects.all()
    shuffled_categories = categories.order_by('?')
    if request.user.is_authenticated:
        count = Cart.cart_count(customer_id=request.user.customer.id)
    else:
        count = cookie_cart(request)
        count = count['count']
    context = {
        'spares' : spares,
        'accessories' : accessories,
        'tyres' : tyres,
        'deals' : deals,
        'count' : count,
        'categories' : categories,
        'shuffled_categories' : shuffled_categories,
    }
    return render(request, 'spares/home.html', context)


def shop(request, id):
    categories = Category.objects.all()
    if request.GET.get('search'):
        search = request.GET.get('search')
        inventory = Inventory.objects.filter(name__icontains=search, category= id) | Inventory.objects.filter(description__icontains=search, category=id)
    else:
        inventory = Inventory.objects.filter(category = id, is_displayed=True, quantity__gt=0)
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
        'categories' : categories,
    }
    return render(request, 'spares/spares.html', context)

def deals(request):
    categories = Category.objects.all()
    inventory = Inventory.objects.filter(has_discount = True, is_displayed=True, quantity__gt=0).order_by("-discount")
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
        'categories' : categories,
    }
    
    return render(request, 'spares/spares.html', context)


def inventory(request, id):
    categories = Category.objects.all()
    item = get_object_or_404(Inventory, id=id)
    inventory = Inventory.objects.filter(category=item.category).order_by('?').exclude(id=item.pk)[:3]
    if request.user.is_authenticated:
        count = Cart.cart_count(customer_id=request.user.customer.id)
    else:
        count = cookie_cart(request)
        count = count['count']
    context = {
        "item" : item,
        "inventory" : inventory,
        "count" : count,
        "categories" : categories,
    }
    return render(request, 'spares/inventory.html', context)

def cart(request):
    categories = Category.objects.all()
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            cart_items = Cart.objects.filter(customer=customer, is_ordered = False).order_by("-id")
            count = Cart.cart_count(customer_id=request.user.customer.id)
            context = {
                "inventory" : cart_items,
                "count" : count,
                "categories" : categories,
            }
        except:
            context = {
                "inventory" : {},
                "count" : 0,
                "categories" : categories,
            }
        
    else:
        context = cookie_cart(request)
        context['categories'] = categories
    
    return render(request, 'spares/cart.html', context)

@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    product_id = data["productId"]
    action = data["action"]
    user = request.user
    product = Inventory.objects.get(id = product_id)
    customer = user.customer
    cart_item, created = Cart.objects.get_or_create(customer = customer, item = product, is_ordered = False)

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
    categories = Category.objects.all()
    if request.method == "POST":
        user = request.user
        form = ShippingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['shipping_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone_number']
            region = form.cleaned_data['region']
            location = form.cleaned_data['shipping_location']
        else:
            print(form.errors)
            message = "Please fill in all the fields"
            messages.error(request, message)
            return render(request, 'spares/checkout.html')
        if request.user.is_authenticated:
            customer = user.customer
            shipping = Shipping(customer = customer, shipping_name = name, phone_number = phone,
                                region = region, shipping_location = location)
            shipping.save()
            cart_items = Cart.objects.filter(customer = customer, is_ordered = False)
            order = Order(customer = customer, shipping_details = shipping)
            order.save()
            order.items.add(*cart_items)
            order.save()
            cart_items.update(is_ordered= True)
            #send_mail([request.user.email],'Order Completed!', 'Thank you for ordering your spare parts with us. Kindly track your order though our website')
            messages.success(request, "Your order has been placed")
            return render(request, 'spares/success.html')
        else:
            customer, created = Customer.objects.get_or_create(name = name, email = email, phone = phone)
            shipping = Shipping(customer = customer, shipping_name = name, phone_number = phone,
                                region = region, shipping_location = location)
            shipping.save()
            results = cookie_checkout(request, customer, shipping)
            return render(request, 'spares/success.html')
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(customer = request.user.customer, is_ordered = False).order_by("-id")
        if cart_items:
            count = sum(cart_items.values_list('quantity', flat=True))

            context = {
                "inventory" : cart_items,
                "count" : count,
                "categories" : categories,
            }
        return render(request, 'spares/checkout.html', context)
    else:
        context = cookie_cart(request)
        return render(request, 'spares/checkout.html', context)

@login_required(login_url='home')
def orders(request):
    categories = Category.objects.all()
    orders = Order.objects.filter(customer = request.user.customer).order_by("-id")
    context = {
        "inventory" : orders,
        "categories" : categories,
    }
    return render(request, 'spares/orders.html', context)

def order(request, id):
    categories = Category.objects.all()
    order = get_object_or_404(Order, id=id)
    context = {
        "orders" : order,
        "categories" : categories,
    }
    return render(request, 'spares/order.html', context)
