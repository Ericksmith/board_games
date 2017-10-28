# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from ..login_reg.models import User
from .models import processCart
from ..store.models import *
from decimal import Decimal


#renders
def cart(request):
    if request.session.get('cart') is not None:
        cart = { '1': 6, '4' : 2 }
        request.session['cart'] = cart
        context = processCart(cart)
        return render(request, 'checkout/cart.html', context)
    return render(request, 'checkout/cart.html')

def confirm(request):
    # if request.session.get('id') is None:
    #     return redirect('/sign-in')
    return render(request, 'checkout/confirm.html')

def order_complete(request):
    # if request.session.get('id') is None:
#     return redirect('/sign-in')
    context = {
        'order': request.session['cart']
    }
    return render(request, 'checkout/order-placed.html', context)

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

def processOrder(request):
    if request.method == 'POST':
        total = 0
        user = User.objects.get(id=request.session['id'])
        current_order = Order(status='Pending', customer=user)
        current_order.save()
        cart = request.session['cart']
        for game_id, count in cart.items():
            current_game = Game.objects.get(id=game_id)
            if current_game.sale_price == '':
                subtotal = Decimal(current_game.price) * count
                SavedPrice.objects.create(price=current_game.price, isSale=False, basePrice=current_game.price, order=current_order, game=current_game)
            else:
                subtotal = Decimal(current_game.sale_price) * count
                SavedPrice.objects.create(price=current_game.sale_price, isSale=True, basePrice=current_game.price, order=current_order, game=current_game)
            total += subtotal
            for i in range(count):
                print(count)
                current_order.items.add(current_game)
        current_order.total=total
        current_order.status='Submitted'
        current_order.save()
        return redirect(order_complete)