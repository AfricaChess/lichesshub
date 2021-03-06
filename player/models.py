# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Player(models.Model):
    handle = models.CharField(max_length=200, unique=True)
    blitz_rating = models.CharField(max_length=10, blank=True)
    verified = models.BooleanField(default=False)

    user = models.ForeignKey(User, null=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.handle
