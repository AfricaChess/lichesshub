# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-10 07:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grandprix', '0003_points'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='tournament_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='grandprix.TournamentType'),
        ),
    ]
