# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User
from ..store.models import Order, Game, ItemInOrder

# Create your models here.


#stand alone functions
def cleanDesc(desc):
    # removes the unicode mark up in the discriptions
    desc = desc.replace('&#10;', ' ')
    desc = desc.replace('&mdash;', ' ')
    desc = desc.replace('&quot;', ' ')
    return desc

def customer(postData):
    return ItemInOrder.objects.filter(order__customer__first_name__contains=postData['search']).all() | ItemInOrder.objects.filter(order__customer__last_name__contains=postData['search']).all()
    # return Order.objects.filter(customer__first_name__contains=postData['search']).all() | Order.objects.filter(customer__last_name__contains=postData['search']).all()

def dateRange(postData):
    pass

def orderId(postData):
    return ItemInOrder.objects.filter(order__id=int(postData['search']))

def game(postData):
    return ItemInOrder.objects.filter(game__title__contains=postData['search']).all()

def findOneOrder(order_id):
    return Order.objects.get(id=order_id)


