# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from player.models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['handle', 'blitz_rating', 'verified']
