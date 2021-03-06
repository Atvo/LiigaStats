# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-22 09:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_shot_goalie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match_id', models.IntegerField()),
                ('season', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Penalty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player', models.CharField(max_length=255)),
                ('infraction', models.CharField(max_length=255)),
                ('time', models.IntegerField()),
            ],
        ),
    ]
