# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *

#algo imports
from random import random, randint
from datetime import datetime, timedelta

# Create your views here.
def index(request):

    def random5(arr):
        if len(arr) <=5:
            return arr
        idx_arr = [randint(0, len(arr)-1)]
        while len(idx_arr) < 5:
            x = randint(0, len(arr)-1)
            exists = False
            for i in idx_arr:
                if x == i:
                    exists = True
            if exists:
                continue
            else:
                idx_arr += [x]    
        return_arr = []
        for i in idx_arr:
            return_arr += [arr[i]]
        return return_arr


    popular_object = {}
    recent_date = datetime.now() - timedelta(days=180)
    recent_orders = Order.objects.filter(created_at__gt=recent_date)
    for order in recent_orders:
        for item in order.items.all():
            if not popular_object[item.id]:
                popular_object[item.id] = 1
            else:
                popular_object[item.id] += 1
    popular5 = []
    while len(popular5)<5:
        high_value = 1
        high_key = 1
        for id in popular_object:
            in_arr = False
            for x in popular5:
                if x.id == id:
                    in_arr = True
                    break
            if in_arr:
                continue
            if popular_object[id] > high_value:
                high_value = popular_object[id]
                high_key = id
        popular5 += [Game.objects.get(id = high_key)]

    if request.session.get('recently_viewed') is None:
        request.session['recently_viewed'] = []

    context = {
        'sale': random5(Game.objects.exclude(sale_price="")),
        'popular': popular5,
        'classics': random5(Game.objects.filter(classic=1)),
        'recent': request.session['recently_viewed']
    }

    return render(request, 'store/index.html', context)

def results(request):

    context = {
        "games": Game.objects.all()
    }

    return render(request, 'store/results.html', context)

def game(request, num):

    context = {
        'game': Game.objects.get(id=num)
    }

    return render(request, 'store/game.html', context)