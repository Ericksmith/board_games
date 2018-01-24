# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import xml.etree.ElementTree as ET
from ..store.models import *
from .models import *
import pickle



#page renders
def dashboard(request):
    return render(request, 'admin/dashboard.html')

def addProduct(request):
    if request.session.get('games_search') is not None:
        context = {
            'games_search': request.session.get('games_search'),
            'selected_game': request.session.get('selected_game')
        }
    else:
        context = {
            'games_search': False,
            'selected_game': request.session.get('selected_game')
        }
    context['categories'] = Catagory.objects.order_by('name')
    return render(request, 'admin/admin_add_game.html', context)

def orders(request):
    if request.session.get('orders') is not None:
        context = {
            'orders': pickle.loads(request.session.get('orders'))
        }
        del request.session['orders']
    else:
        context = {
            'orders': ItemInOrder.objects.order_by('-id')[:10]
        }
    return render(request, 'admin/orders.html', context)

def edit_order(request, order_id):
    context = {
        "order": findOneOrder(order_id)
    }
    return render(request, "admin/edit_order.html", context)

def edit_game(request, game_id):
    context = {
        "game": Game.objects.get(id=game_id),
        "categories": Catagory.objects.all(),
    }
    return render(request, 'admin/admin_edit.html', context)

#Form processing
def searchProducts(request):
    if request.method == 'POST':
        request.session['games_search'] = apiSearch(request.POST)
        return redirect(addProduct)

def select_game(request, game_id):
    ''' Queries the Board game geek API by the game id param and returns
    that games info as a dictionary to be rendered on the add product page.'''
    request.session['selected_game'] = api_game_select(game_id)
    return redirect(addProduct)


def create_game(request):
    if request.method == 'POST':
        errors = Game.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(addProduct)
        data = request.POST
        if data.get('classic') == 'True':
            classic = True
        else:
            classic = False

        try:
            newGame = Game(title = data['title'], publisher = data['publisher'], rating=data['rating'], rank=data['rank'], yearpublished = int(data['yearpublished']), thumbnail= data['thumbnail'], image=data['image'], minplayers= int(data['minplayers']), maxplayers = int(data['maxplayers']), playtime = int(data['playtime']), description= data['description'], price= data['price'], sale_price= data['sale_price'], classic = classic)
            newGame.save()
            cats = data.getlist('category')
            for cat in cats:
                cat_to_add = Catagory.objects.get(id=(int(cat)))
                newGame.catagory.add(cat_to_add)
                newGame.save()
            newGame.save()
        except:
            messages.error(request, 'Unable to add game, please check all fields')
            return redirect(addProduct)

        messages.success(request, 'Game added')
        return redirect(addProduct)

def update_game(request):
    if request.method == 'POST':
        errors = Game.objects.validator(request.POST)
        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect(addProduct)
        data = request.POST
        if data.get('classic') == 'True':
            classic = True
        else:
            classic = False
        # try:
        update = Game.objects.get(id=data['id'])
        update.title = data['title']
        update.publisher = data['publisher']
        update.yearpublished = int(data['yearpublished'])
        update.rating=data['rating']
        update.image=data['image']
        update.minplayers= int(data['minplayers'])
        update.maxplayers = int(data['maxplayers'])
        update.playtime = int(data['playtime'])
        update.description= data['description']
        update.price= data['price']
        if data['sale_price'] == "" or not 'sale_price' in data:
            update.sale_price = ''
        else:
            update.sale_price = str(data['sale_price'])
        update.classic = classic
        update.save()

        old_cats = Game.objects.get(id=data['id']).catagory.all()
        old_cat_ids = []
        for cat in old_cats:
            old_cat_ids += [cat.id]
        new_cat_ids = data.getlist('category')

        for ocat in old_cat_ids:
            update.catagory.remove(Catagory.objects.get(id=int(ocat)))

        for ncat in new_cat_ids:
            update.catagory.add(Catagory.objects.get(id=int(ncat)))

        # except:
        #     messages.error(request, 'Unable to update game, please check all fields')
        #     return redirect('/admin/edit-game/{}'.format(data['id']))

        messages.success(request, 'Game updated')
        return redirect('/admin/edit-game/{}'.format(data['id'])) 


    
def editSearch(request):
    #single game in context will be called "game" 
    pass

def orderSearch(request):
    if request.method == 'POST':
        search_type = request.POST['search_type']
        searchFunctions = {
            'customer': customer(request.POST),
            'dateRange': dateRange(request.POST),
            'orderId': orderId(request.POST),
            'game': game(request.POST)
        }
        request.session['orders'] = pickle.dumps(searchFunctions[search_type])
        return redirect("/admin/orders")

def update_order(request):
    if request.method == "POST":
        print(request.POST)
        orderUpdater(request.POST)
        return redirect("/admin/edit-order/{}".format(request.POST['orderId']))

    