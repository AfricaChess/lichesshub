from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
#from account.models import Account


class Club(models.Model):
    name = models.CharField(max_length=100)
    #account = models.ForeignKey(Account)
    captain = models.ForeignKey(User, null=True)
    last_sync = models.DateTimeField(default=timezone.now)

    def __unicode__(self):
        return self.name.replace('-', ' ').upper()


class Member(models.Model):
    handle = models.CharField(max_length=200, unique=True)
    blitz_rating = models.CharField(max_length=10, blank=True)
    club = models.ForeignKey(Club)
    order = models.PositiveIntegerField('Board Order', null=True, blank=True)

    def __unicode__(self):
        return self.handle
