# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-26 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_auto_20171026_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='price',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='game',
            name='sale_price',
            field=models.CharField(max_length=30),
        ),
    ]
