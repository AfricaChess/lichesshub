# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-05 04:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournament', '0008_auto_20171205_0409'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='tournamentround',
            unique_together=set([('tournament', 'tag')]),
        ),
    ]
