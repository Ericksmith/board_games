# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User
from ..store.models import Order, Game, ItemInOrder
import requests
import xml.etree.ElementTree as ET
import json

# Create your models here.


#stand alone functions
def cleanDesc(desc):
    # removes the unicode mark up in the discriptions
    desc = desc.replace('&#10;', ' ')
    desc = desc.replace('&mdash;', ' ')
    desc = desc.replace('&quot;', ' ')
    return desc

#4 functions that the admin picks to search for an order by. 
def customer(postData):
    return ItemInOrder.objects.filter(order__customer__first_name__contains=postData['search']).all() | ItemInOrder.objects.filter(order__customer__last_name__contains=postData['search']).all()

def dateRange(postData):
    pass

def orderId(postData):
    if postData['search'].isdigit():
        return ItemInOrder.objects.filter(order__id=int(postData['search']))
    return {}

def game(postData):
    return ItemInOrder.objects.filter(game__title__contains=postData['search']).all()

#api functions
def apiSearch(postData):
    # Searches BBG api for a game and return a list of matching games
    # postData = a name of a game the admin enters
    print "apiSearch"
    searchResults = requests.get("https://www.boardgamegeek.com/xmlapi/search?search={}".format(postData['search']))
    root = ET.fromstring(searchResults.content)
    games_list = []
    for game in root:
        title = game.find('name').text
        try:
            year_published = game.find('yearpublished').text
        except:
            year_published = 'Unknown'
        id = game.attrib['objectid']
        games_list.append({
            'id' : id,
            'title': title,
            'year_published' : year_published,
        })
    return games_list

def api_game_select(game_id):
    resp = requests.get("https://bgg-json.azurewebsites.net/thing/{}".format(game_id))
    game = json.loads(resp.text)
    desc = game['description']
    desc = cleanDesc(desc)
    game_to_add = {
        'playtime': game['playingTime'],
        'minplayers': game['minPlayers'],
        'maxplayers': game['maxPlayers'],
        'description': desc,
        'thumbnail': game['thumbnail'],
        'image': game['image'],
        'yearpublished': game['yearPublished'],
        'title': game['name'],
        'publisher': game['publishers'][0],
        'rating': str(int(game['bggRating'])),
        'rank': game['rank']
    }
    return game_to_add


def orderUpdater(postData):
    order = findOneOrder(postData['orderId'])
    for key, val in postData.items():
        if val == "on":
            print('refund')
    #unfinished function. Will update order from the edit-order page.
    #refund will bring the price to zero? Is refund even needed?
    pass



def findOneOrder(order_id):
    return Order.objects.get(id=order_id)


