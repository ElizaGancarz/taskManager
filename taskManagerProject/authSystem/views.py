from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

#czy hasła są takie same
#czy username wolny
#czy email wolny
#walidacja maila (domena)
#walidacja hasła
 

def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    # pass the regular expression
    # and the string into the fullmatch() method
    if (re.fullmatch(regex, email)):
        return True
    else:
        return False


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {'form': RegisterForm()})
    else:  # POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            usernameTaken = User.objects.filter(username=username).exists()
            emailTaken = User.objects.filter(email=email).exists()
            if emailTaken:
                error = 'This email is already taken. Try again.'
            if usernameTaken:
                error = 'This username is already taken. Try again.'

            if not emailTaken and not usernameTaken:
                emailValid = check_email(email)
                if emailValid:
                    try:
                        validate_password(password1)
                    except ValidationError as e:
                        return render(request, 'register.html', {'passwordErrors': e.messages, 'form': RegisterForm()})
                    else:
                        user = User.objects.create_user(username, email, password1)
                        return redirect('home')
                else:
                    error = 'Invalid email. Try again.'
        else:
            error = 'Your passwords did not match. Try again.'

        return render(request, 'register.html', {'error': error, 'form': RegisterForm()})
    

def login_user(request):
    if request.method == 'GET':
        return render(request, 'login_user.html', {'form': AuthenticationForm()})
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            usernameExist = User.objects.filter(username=username).exists()
            if usernameExist:
                error = 'Incorrect password.'
            else:
                error = 'No such user in database.'
            return render(request, 'login_user.html', {'error': error, 'form': AuthenticationForm()})

             
def logout_user(request):
    logout(request)
    return redirect('home')