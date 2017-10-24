# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.
def sign_in(request):
    return render(request, 'login_reg/sign-in.html')