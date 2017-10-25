# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
# from login_reg.models import User
import requests
import xml.etree.ElementTree as ET

# Create your views here.

#page renders
def dashboard(request):
    if request.session.get('games_search') is not None:
        context = {
            'games_search': request.session['games_search']
        }
        del request.session['games_search']
    else:
        context = {
            'games_search': False
        }
    return render(request, 'admin/dashboard.html', context)

def addProduct(request):
    pass

def orders(request):
    pass


#Form processing
def searchProducts(request):
    if request.method == 'POST':
        searchResults = requests.get("https://www.boardgamegeek.com/xmlapi/search?search=risk")
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
        return redirect(dashboard)