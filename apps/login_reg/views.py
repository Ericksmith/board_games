# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def sign_in(request, page_id=10):
    request.session['page_id'] = page_id
    print(request.session['page_id'])
    return render(request, 'login_reg/sign-in.html')



#login-reg-logout managers
def register(request):
    if request.method == 'POST':
        errors = User.objects.validator(request.POST)
        if errors.get('password') is not None or errors['error']:
            if errors['error']:
                for error in errors['error']:
                    messages.error(request, error)
            if errors.get('password') is not None:
                for error in errors['password']:
                    messages.error(request, error)
            return redirect('/sign-in/' + request.session.get('page_id'))
    hashed_password = User.objects.password_hasher(request.POST['password'])
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],  password=hashed_password)
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    if request.session.get('page_id') == '1':
        return redirect('/checkout/cart')
    else:
        return redirect('/')

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            if User.objects.password_checker(request.POST['password'], user[0].password):
                request.session['id'] = user[0].id
                if request.session.get('page_id') == '1':
                    return redirect('/checkout/cart')
                else:
                    return redirect('/')
            else:
                return redirect(sign_in)
        else:
            messages.warning(request, 'Email did not match password')
            return redirect(sign_in)

def logout(request):
    del request.session['id']
    return redirect('/')