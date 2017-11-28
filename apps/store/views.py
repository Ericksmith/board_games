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
            if not item.game_id in popular_object:
                popular_object[item.game_id] = item.quantity
            else:
                popular_object[item.game_id] += item.quantity

    popular5 = []
    while len(popular5)<5:
        high_value = 1
        high_key = 1
        for game_id in popular_object:
            in_arr = False
            for i in popular5:
                if game_id == i.id:
                    in_arr = True
                    break
            if in_arr:
                continue
            if popular_object[game_id] > high_value:
                high_value = popular_object[game_id]
                high_key = game_id
        popular5 += [Game.objects.get(id = high_key)]

    context = {
        'sale': random5(Game.objects.exclude(sale_price="")),
        'popular': popular5,
        'classics': random5(Game.objects.filter(classic=1)),
        'categories': Catagory.objects.order_by("name"),
    }

    if 'recently_viewed_ids' in request.session:
        rv_list = []
        for i in request.session['recently_viewed_ids']:
            rv_list += [Game.objects.get(id=i)]
        context['recently_viewed'] = rv_list

    return render(request, 'store/index.html', context)

def results(request):
    games = []
    if 'search_results' in request.session:
        for game_id in request.session['search_results']:
            games.append(Game.objects.get(id=game_id)) 
            games = sorted(games, key=lambda game: game.title)
    else:
        games = Game.objects.order_by("name")

    context = {
        'categories': Catagory.objects.order_by("name"),
        "games": games
    }

    return render(request, 'store/results.html', context)

def game(request, num):

    if not 'recently_viewed_ids' in request.session:
        request.session['recently_viewed_ids'] = [num]
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
        'game': Game.objects.get(id=num),
        'categories': Game.objects.get(id=num).catagory.order_by('name')
    }

    print context['categories']

    return render(request, 'store/game.html', context)

def user(request, user_id):
    if not 'id' in request.session:
        return redirect('/')
    if request.session['id'] != int(user_id):
        return redirect('/')

    context = {
        "user": User.objects.get(id = request.session['id']),
        "orders": Order.objects.filter(customer_id = request.session['id'])
    }

    return render(request, 'store/user.html', context)

def add_to_cart(request):

    if not 'cart' in request.session:
        request.session['cart'] = {str(request.POST['game_id']): 1}
    else:
        if not request.POST['game_id'] in request.session['cart']:
            request.session['cart'].update({str(request.POST['game_id']): 1}) 
        else: 
            request.session['cart'][str(request.POST['game_id'])] += 1
    request.session.modified = True

    return redirect('/checkout/cart')

def results_process(request):
    results = []
    if 'category_id' in request.POST:
        games = Game.objects.filter(catagory=request.POST['category_id'])
        for game in games:
            results.append(game.id)
        request.session['search_results'] = results
        request.session['search_label'] = Catagory.objects.get(id=request.POST['category_id']).name

    return redirect('/results')

def view_all(request):
    request.session['search_results'] = []
    games = Game.objects.order_by('title')
    for game in games:
        request.session['search_results'].append(game.id)
    request.session['search_label'] = "All Games"
    return redirect('/results')



