# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from ..login_reg.models import User
from ..store.models import *

# Create your views here.
def cart(request):
    return render(request, 'checkout/cart.html')

def checkout(request):

    return render(request, 'checkout/checkout.html')