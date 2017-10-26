# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# Create your models here.


#stand alone functions
def cleanDesc(desc):
    desc = desc.replace('&#10;', ' ')
    desc = desc.replace('&mdash;', ' ')
    desc = desc.replace('&quot;', ' ')
    return desc