# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from ..login_reg.models import User


#Managers
class GameManager(models.Manager):
    def validator(request, postData):
        pass

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Game(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    yearpublished = models.SmallIntegerField()
    minplayers = models.SmallIntegerField()
    maxplayers = models.SmallIntegerField()
    playtime = models.SmallIntegerField()
    description = models.TextField()
    price = models.CharField(max_length=30)
    sale_price = models.CharField(max_length=30)
    thumbnail = models.URLField(max_length=255)
    image = models.URLField(max_length=255)
    rank = models.CharField(max_length=30, default='80')
    rating = models.CharField(max_length=30, default='7')
    classic = models.BooleanField()
    rank = models.CharField(max_length=75)
    rating = models.CharField(max_length=75)
    catagory = models.ManyToManyField(Catagory, related_name='games')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = GameManager()


class Order(models.Model):
    status = models.CharField(max_length=255)
    total = models.CharField(max_length=30)
    customer = models.ForeignKey(User, related_name='user_orders')
    items = models.ManyToManyField(Game, related_name='game_orders')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

class SavedPrice(models.Model):
    """Price of the product at check out.Price = what the costumer paid
    basePrice = the non sale price. isSale = was the item on sale."""
    price = models.CharField(max_length=30)
    isSale = models.BooleanField(default=False)
    basePrice = models.CharField(max_length=30)
    game = models.ForeignKey(Game, related_name='previous_price')
    order = models.ForeignKey(Order, related_name='price_at_purchase')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
