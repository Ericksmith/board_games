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
    if request.session.get('cart') is None:
        # cart = request.session['cart']
        cart = { '1': 1, '2' : 2 }
        games_to_buy = []
        x = 0
        total = 0
        for id, count in cart.items():
            if count == 0:
                continue
            x += 1
            current_game = Game.objects.get(id=id)
            print(current_game.sale_price)
            if current_game.sale_price == '':
                subtotal = Decimal(current_game.price) * count
            else:
                subtotal = Decimal(current_game.sale_price) * count
            itemnum = 'item' + str(x)
            total += subtotal
            quantity = ''
            for i in range(count, -1, -1):
                quantity += '<option value="{}">{}</option>'.format(str(i-current_game.id), str(i))
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
    
    return render(request, 'checkout/confirm.html')

def order_placed(request):
    return render(request, 'checkout/order-placed.html')

#processes
def update_cart(request):
    print('update')
    if request.method == 'POST':
        pass
    return redirect(cart)