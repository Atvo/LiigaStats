# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 09:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_shot_blocker'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='first_assist',
            field=models.CharField(default=b'Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='shot',
            name='second_assist',
            field=models.CharField(default=b'Unknown', max_length=255),
        ),
    ]