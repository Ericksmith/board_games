# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, redirect
# from login_reg.models import User
import requests
import xml.etree.ElementTree as ET

# Create your views here.

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

    # selected_game = requests.get("https://www.boardgamegeek.com/xmlapi/boardgame/{}".format(game_id))
    # game = ET.fromstring(selected_game.content)
    # game_to_add = {
    #     'playtime': game[0].find('playingtime').text,
    #     'minplayers': game[0].find('minplayers').text,
    #     'maxplayers': game[0].find('maxplayers').text,
    #     'description': game[0].find('description').text,
    #     'thumbnail': game[0].find('thumbnail').text,
    #     'image': game[0].find('image').text,
    #     'yearpublished': game[0].find('yearpublished').text,
    #     'title': game[0].find('name').text,
    #     'publisher': game[0].find('boardgamepublisher').text,
    # }
    request.session['selected_game'] = game_to_add
    return redirect(addProduct)