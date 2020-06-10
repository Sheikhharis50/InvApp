from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import os
import copy
import pickle
import pandas as pd
from cryptography.fernet import Fernet
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.conf import settings
from datetime import datetime, timedelta
import time


def login(request):
    try:
        if (not request.session.get('flag') is None):
            return redirect('index')
        if request.method == 'POST':
            # get form values
            username = request.POST['username']
            password = request.POST['password']
            remember = request.POST.getlist('remember')
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                response = redirect('index')
                request.session['remember'] = ''
                request.session['flag'] = 'flag'
                # setting for remember me
                if len(remember) == 1:
                    request.session['remember'] = 'remember'
                auth.login(request, user)
                messages.success(request, 'Success! You are now logged in')
                return response
            
            messages.error(request, 'Error! User does not exists')
            return redirect('login')
        else:
            return render(request, 'accounts/login.html')
    except:
        messages.error(request, 'Error! System is not responding')
        return render(request, 'accounts/login.html')

def logout(request):
    
    response = redirect('login')
    if request.method == 'POST':
        if not request.session.get('flag') is None:
            del request.session['flag']
        auth.logout(request)
        messages.success(request, "Success! You are now logged out")
    return response

def check_status(request):
    last_activity = request.session.get('last_activity')
    if last_activity != None:
        last_activity = datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.now()
        mints_until_now = (now - last_activity).seconds/60
        print("")
        print(mints_until_now, " min is done")
        print("")
        if mints_until_now >= 5.0:
            response = JsonResponse({'message':'Session Extended to 5 min!'})
            request.session['last_activity'] = str(datetime.now())
            set_cookie(response, 'sessionid', request.COOKIES['sessionid'], 1, 1, mints_until_now + 5.0)
            return response
        return JsonResponse({'message': f'{mints_until_now} min is done!'})
    return JsonResponse({'message': 'Remember Me is Selected!'})

def setCookieExpiry(request):
    response = JsonResponse({'val':'created'})
    if request.session['remember'] == 'remember':
        seconds = 15 * 24 * 60 * 60
        response.set_cookie('sessionid', request.COOKIES['sessionid'], max_age=seconds)
        request.session['remember'] = ''
        
    return response

def register(request):
    if request.method == 'POST':
        # get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # check if passwords are matched
        if password == password2:
            # Check Username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # Check email
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('register')
                else:
                    # Looks Good
                    user = User.objects.create_user(username=username,
                                                    password=password, email=email,
                                                    first_name=first_name, last_name=last_name)
                    user.save()
                    messages.success(request, 'You are now Registered')
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def encrypt(password):
    encoded = password.encode()
    key = Fernet.generate_key()

    pass

def decrypt(encrypt_password):

    pass

def set_cookie(response, key, value, days_expire=7, hrs_expire=24, min_expire=60, sec_expire=60):
    
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * hrs_expire * min_expire * sec_expire
    print("Cookie Status:\nMax_Age: ", max_age, " secs")
    expires = datetime.strftime(datetime.utcnow() + timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
    print("Expires on: ", expires, "\n")
    response.set_cookie(key, value, max_age=max_age, expires=expires,
                        domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def create_new_file(path):
    users = [['garbage', 'garbage']]
    f = open(path, 'wb')
    pickle.dump(users, f)
    f.close()

def dump_to_file(users, path):
    f = open(path, 'wb')
    pickle.dump(users, f)
    f.close()

def load_from_file(path):
    f = open(path, 'rb')
    users = pickle.load(f)
    f.close()
    return users
