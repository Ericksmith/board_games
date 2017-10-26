# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, redirect
from django.contrib import messages
import requests
import xml.etree.ElementTree as ET
from ..store.models import *
from ..login_reg.models import User
from PIL import Image



#page renders
def dashboard(request):
    return render(request, 'admin/dashboard.html')

def addProduct(request):
    if request.session.get('games_search') is not None:
        context = {
            'games_search': request.session['games_search']
        }
        del request.session['games_search']
    else:
        context = {
            'games_search': False,
            'selected_game': request.session['selected_game']
        }
    return render(request, 'admin/admin_add_game.html', context)

def orders(request):
    pass


#Form processing
def searchProducts(request):
    if request.method == 'POST':
        searchResults = requests.get("https://www.boardgamegeek.com/xmlapi/search?search={}".format(request.POST['search']))
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
            request.session['games_search'] = games_list
        return redirect(addProduct)

def select_game(request, game_id):
    resp = requests.get("https://bgg-json.azurewebsites.net/thing/{}".format(game_id))
    game = json.loads(resp.text)
    print(game)
    game_to_add = {
        'playtime': game['playingTime'],
        'minplayers': game['minPlayers'],
        'maxplayers': game['maxPlayers'],
        'description': game['description'],
        'thumbnail': game['thumbnail'],
        'image': game['image'],
        'yearpublished': game['yearPublished'],
        'title': game['name'],
        'publisher': game['publishers'][0],
        'rating': game['bggRating'],
        'rank': game['rank']
    }
    request.session['selected_game'] = game_to_add
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
        newGame = Game(title = data['title'], publisher = data['publisher'], yearpublished = int(data['yearpublished']), minplayers= int(data['minplayers']), maxplayers = int(data['maxplayers']), playtime = int(data['playtime']), description= data['description'], price= int(data['price']), sale_price= float(data['sale_price']), classic = classic)
        newGame.save()
        # **********TOO BE ADDED LATER***********
        #  thumbnail= data['thumbnail'], image=data['image'],
        # cats = data.POST['catagory']
        # # for cat in cats:
        # #     cat_to_add = Catagory.objects.filter(name=cat)
        # #     newGame.add(cat_to_add)
        return redirect(dashboard)
