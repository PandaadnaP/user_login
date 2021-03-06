# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-17 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER_login', '0019_auto_20170417_1533'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='difficulty',
            name='id',
        ),
        migrations.AlterField(
            model_name='difficulty',
            name='chapterid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='difficulty',
            name='userid',
            field=models.IntegerField(primary_key=True),
        ),
        migrations.AlterModelTable(
            name='chapters',
            table='chapters',
        ),
        migrations.AlterModelTable(
            name='modules',
            table='modules',
        ),
        migrations.AlterModelTable(
            name='parts',
            table='parts',
        ),
        migrations.AlterModelTable(
            name='questions',
            table='questions',
        ),
    ]
