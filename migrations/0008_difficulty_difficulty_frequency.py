# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER_login', '0007_auto_20170417_1444'),
    ]

    operations = [
        migrations.AddField(
            model_name='difficulty',
            name='difficulty_frequency',
            field=models.IntegerField(default=100),
        ),
    ]
