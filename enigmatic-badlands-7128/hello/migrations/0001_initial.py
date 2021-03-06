# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-19 15:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Greeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField(auto_now_add=True, verbose_name=b'date created')),
            ],
        ),
        migrations.CreateModel(
            name='Shot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shooter', models.TextField()),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('time_min', models.IntegerField()),
                ('time_sec', models.IntegerField()),
                ('shooting_team', models.TextField()),
                ('opposing_team', models.TextField()),
                ('outcome', models.TextField()),
            ],
        ),
    ]
