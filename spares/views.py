from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Inventory

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

def checkout(request):
    return render(request, 'spares/checkout.html')

def spares(request):
    inventory = Inventory.objects.filter(is_displayed=True, quantity__gt=0).order_by('name')
    context = {
        'inventory' : inventory,
    }
    return render(request, 'spares/spares.html', context)

