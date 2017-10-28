from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


POINTS_MAP = {
    1: 100,
    2: 90,
    3: 80,
    4: 70,
    5: 60,
    6: 50,
    7: 40,
    8: 30,
    9: 20,
    10: 10
}


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    synced = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=100)
    # score = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.name

    @property
    def score(self):
        scores = PlayerScore.objects.filter(player=self).order_by('-points')
        return sum(i.points for i in scores[:10])


class PlayerScore(models.Model):
    player = models.ForeignKey(Player)
    tournament = models.ForeignKey(Tournament)
    rank = models.PositiveIntegerField()
    points = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return unicode(self.player)
