# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-02 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('player', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='verified',
            field=models.BooleanField(default=True),
        ),
    ]