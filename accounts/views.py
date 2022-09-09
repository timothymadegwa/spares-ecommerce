from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User, FailedLogin
from accounts.forms import LoginForm, RegistrationForm
from django.conf import settings

from difflib import SequenceMatcher
from validate_email import validate_email

# Create your views here.
def similar(password, user_field):
    # checking for the similarity ratio between given fields
    return SequenceMatcher(None, password, user_field).ratio()

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


def register(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        if request.method == "POST":
            context = {'values': request.POST}
            tac = request.POST['tac']

            if tac == 'on':
                tac = True
            else:
                message = "You did not accept the Terms and Conditions"
                messages.error(request, message)
                return render(request, 'spares/login.html')

            form = RegistrationForm(request.POST)
            if form.is_valid():
                f_name = form.cleaned_data['first_name']
                l_name = form.cleaned_data['last_name']
                email = form.cleaned_data['email'].lower()
                phone = form.cleaned_data['phone']
                password = form.cleaned_data['password']
                confirm_password = form.cleaned_data['confirm_password']
            else:
                message = "Please fill in all the fields"
                messages.error(request, message)
                return render(request, 'spares/login.html')

            if password == confirm_password:
                if len(password) < 8:
                    message = "Kindly ensure that your password is 8 characters or more"
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)

                if similar(password, f_name) > 0.49:
                    message = "Password is too similar to your First Name"
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)

                if similar(password, l_name) > 0.49:
                    message = "Password is too similar to your Last Name"
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)

                if similar(password, email) > 0.49:
                    message = "Password is too similar to your E-mail address"
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)

                if not validate_email(email):
                    message = 'The Email format is wrong'
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)

                if User.objects.filter(email=email).exists():
                    message = 'The Email address already has an existing account'
                    messages.error(request, message)
                    return render(request, 'spares/login.html', context)
                    
                else:
                    user = User.objects.create_user(first_name=f_name, last_name=l_name, email=email, phone=phone, password=password)
                    user.save()
                    current_site = get_current_site(request)
                    email_subject = "Welcome!"
                    context = { 'user' : user,
                                'domain' : current_site.domain,
                                }
                    email_body = render_to_string('spares/email.html', context)
                    mail = EmailMessage(
                        email_subject,
                        email_body,
                        settings.EMAIL_HOST_USER,
                        [email]
                    )
                    mail.send()
                    message = 'Congragulations! You are now registered! Please login '
                    messages.success(request, message)
                    return redirect('login')
            else:
                message = 'Passwords do not match'
                messages.error(request, message)
                return render(request, 'spares/login.html', context)
        return render(request, 'spares/login.html')

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        message = "You have been logged out"
        messages.success(request, message)
        return redirect('login')