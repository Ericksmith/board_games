# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Catagory(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Game(models.Model):
    title = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    yearpublished = models.DateField()
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

