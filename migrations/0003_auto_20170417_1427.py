# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 14:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('USER_login', '0002_auto_20170417_1416'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cut',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='difficulty',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='wrongquestions',
            options={'managed': False},
        ),
    ]
