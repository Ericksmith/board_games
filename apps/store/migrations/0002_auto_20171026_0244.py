# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-26 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='publisher',
            field=models.SmallIntegerField(),
        ),
    ]
