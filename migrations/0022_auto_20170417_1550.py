# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 15:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('USER_login', '0021_auto_20170417_1549'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='difficulty',
            table='USER_login_difficulty',
        ),
    ]
