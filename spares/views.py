from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request, 'spares/login.html')

# @login_required(login_url='login')
def home(request):
    return render(request, 'spares/home.html')

def cart(request):
    return render(request, 'spares/cart.html')

def checkout(request):
    return render(request, 'spares/checkout.html')

def spares(request):
    return render(request, 'spares/spares.html')

