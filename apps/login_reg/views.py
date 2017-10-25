# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def sign_in(request):
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
            return redirect#(####FILL IN###)
    hashed_password = User.objects.password_hasher(request.POST['password'])
    User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], birthday=request.POST['birthday'], password=hashed_password)
    request.session['id'] = User.objects.get(email=request.POST['email']).id
    return redirect#(####FILL IN###)

def login(request):
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            if User.objects.password_checker(request.POST['password'], user[0].password):
                request.session['id'] = user[0].id
                return redirect#(####FILL IN###)
            else:
                return redirect#(####FILL IN###)
        else:
            messages.warning(request, 'Email did not match password')
            return redirect#(####FILL IN###)

def logout(request):
    del request.session['id']
    return redirect#(####FILL IN###)