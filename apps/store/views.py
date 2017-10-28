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

    context = {
        'sale': random5(Game.objects.exclude(sale_price="")),
        'popular': popular5,
        'classics': random5(Game.objects.filter(classic=1)),
        'categories': Catagory.objects.all(),
    }

    if 'recently_viewed_ids' in request.session:
        rv_list = []
        for i in request.session['recently_viewed_ids']:
            rv_list += [Game.objects.get(id=i)]
        context['recently_viewed'] = rv_list

    return render(request, 'store/index.html', context)

def results(request):

    if 'id' in request.session:
        del request.session['id']
        print 'session id deleted'

    if 'cart' in request.session:
        del request.session['cart']
        print "deleted cart"

    context = {
        'categories': Catagory.objects.all(),
        "games": Game.objects.all()
    }

    return render(request, 'store/results.html', context)

def game(request, num):

    if not 'id' in request.session:
        print 'session id created'
        request.session['id'] = 1

    if not 'recently_viewed_ids' in request.session:
        print "create rv firing"
        request.session['recently_viewed_ids'] = [num]
        print request.session['recently_viewed_ids']
    else:
        exists = False
        for i in request.session['recently_viewed_ids']:
            if i == num:
                exists = True
        if not exists:
            request.session['recently_viewed_ids'].insert(0, num) 
        while len(request.session['recently_viewed_ids']) > 5:
            request.session['recently_viewed_ids'].pop()
        request.session.modified = True


    context = {
        'game': Game.objects.get(id=num)
    }

    return render(request, 'store/game.html', context)

def user(request, user_id):




    return render(request, 'store/user.html')

def add_to_cart(request):

    if not 'cart' in request.session:
        request.session['cart'] = {str(request.POST['game_id']): 1}
    else:
        if not request.POST['game_id'] in request.session['cart']:
            print "not in cart"
            request.session['cart'].update({str(request.POST['game_id']): 1}) 
        else: 
            request.session['cart'][str(request.POST['game_id'])] += 1

    print "cart"
    print request.session['cart']
    request.session.modified = True

    return redirect('/checkout/cart')

def results_process(request):

    return redirect('/results')




