# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0011_auto_20171208_0427'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='completed',
            field=models.BooleanField(default=False),
        ),
    ]
