# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime


class Account(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    registered_on = models.DateTimeField(default=timezone.now)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    CREDIT = 0
    DEBIT = 1

    TRANS_TYPE = enumerate(('Credit', 'Debit'))

    account = models.ForeignKey(Account)
    kind = models.PositiveIntegerField(choices=TRANS_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    trans_date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(blank=True)
    processed = models.BooleanField(default=False)

    def __unicode__(self):
        return unicode(self.account)


class Game(models.Model):
    white = models.CharField(max_length=100)
    black = models.CharField(max_length=100)
    white_score = models.FloatField(null=True, blank=True)
    black_score = models.FloatField(null=True, blank=True)
    game_date = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return u'{} vs {}'.format(self.white, self.black)
