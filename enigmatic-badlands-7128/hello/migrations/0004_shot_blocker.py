# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-21 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_auto_20160120_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='shot',
            name='blocker',
            field=models.CharField(default=b'Unknown', max_length=255),
        ),
    ]
