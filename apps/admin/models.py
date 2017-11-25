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

def queryToDict(query):
    result = {}
    innerList = []
    for item in query:
        innerList.append(item)
    # result = {
    #     'search': innerList
    # }
    print('toDict', innerList)
    return innerList

def customer(postData):
    search = Order.objects.filter(customer__first_name__contains=postData['search']) | Order.objects.filter(customer__last_name__contains=postData['search'])
    return search

def dateRange(postData):
    pass

def orderId(postData):
    pass

def game(postData):
    pass


