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
    price = models.SmallIntegerField()
    sale_price = models.SmallIntegerField()
    thumbnail = models.ImageField()
    image = models.ImageField()
    classic = models.BooleanField()
    catagory = models.ManyToManyField(Catagory, related_name='games')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    objects = GameManager()

class Order(models.Model):
    status = models.CharField(max_length=255)
    items = models.ForeignKey(Game, related_name='games_orders')
    customer = models.ForeignKey(User, related_name='users_orders')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)