from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from .models import User, FailedLogin
from accounts.forms import LoginForm

# Create your views here.
def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            user = None
            form = LoginForm(request.POST)

            #checking for form validity
            if form.is_valid():
                email = form.cleaned_data['email'].lower()
                password = form.cleaned_data['password']

                if not User.objects.filter(email=email).exists():
                    message = 'User does not exist!'
                    messages.error(request, message)
                    return render(request, 'spares/login.html')

                user = auth.authenticate(email=email, password=password)

            if user is not None:
                auth.login(request, user)
                message = 'You are now logged in!'
                messages.success(request, message)
                return redirect('home')
            else:
                failed_user = get_object_or_404(User, email = email)
                failed_login = FailedLogin(user=failed_user, reason="Incorrect account password")
                failed_login.save()
                message = 'Invalid credentials. Enter correct username and password'
                messages.error(request, message)
                return render(request, 'spares/login.html')
        return render(request, 'spares/login.html')

