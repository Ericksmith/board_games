# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.models import User
from ..store.models import *
from decimal import Decimal


# Create your views here.

#renders
def cart(request):
    if request.session.get('cart') is not None:
        cart = { '1': 1, '2' : 2 }
        # cart = request.session['cart']
        games_to_buy = []
        x = 0
        total = 0
        for id, count in cart.items():
            if count == 0:
                continue
            x += 1
            current_game = Game.objects.get(id=id)
            if current_game.sale_price == '':
                subtotal = Decimal(current_game.price) * count
            else:
                subtotal = Decimal(current_game.sale_price) * count
            itemnum = 'item' + str(x)
            total += subtotal
            quantity = ''
            for i in range(count, -1, -1):
                quantity += '<option value="{}">{}</option>'.format(str(i) + '-' + str(current_game.id), str(i))
            games_to_buy.append(
                {
                    'game_object': current_game,
                    'quantity' : quantity,
                    'subtotal' : '$'+str(subtotal),
            })
        context = {
            'total' : '$'+str(total),
            'list_of_games' : games_to_buy
        }
        return render(request, 'checkout/cart.html', context)
    return render(request, 'checkout/cart.html')

def confirm(request):
    # if request.session.get('id') is None:
    #     return redirect('/sign-in')
    return render(request, 'checkout/confirm.html')

def order_placed(request):
    return render(request, 'checkout/order-placed.html')

#processes
def update_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        for key in request.POST:
            if key[0]=='o':
                data = request.POST[key].split('-')
                quantity = data[0]
                game_id = data[1]
                request.session['cart'].update({str(game_id): int(quantity)})
                print(request.session['cart'])
        return redirect(cart)
    return redirect(cart)