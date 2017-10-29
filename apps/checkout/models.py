# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..store.models import *
from ..login_reg.models import User
from decimal import Decimal


#stand alone functions
def processCart(cart):
    # cart = { '1': 4, '2' : 2 }
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
    return {
        'total' : '$'+str(total),
        'list_of_games' : games_to_buy,
        'order' : cart,
    }

def createOrder(cart):
    pass

# Create your models here.
