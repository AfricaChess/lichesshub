from __future__ import unicode_literals

from django.db import models
from django.db.models.aggregates import Sum

from club.models import Club, Member


class Tournament(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class TournamentRound(models.Model):
    tournament = models.ForeignKey(Tournament)
    tag = models.CharField(max_length=100)

    def __unicode__(self):
        return '{} ({})'.format(self.tournament.name, self.tag)


class Match(models.Model):
    PENDING = 0
    STARTED = 1
    COMPLETED = 2

    STATUSES = enumerate(('Pending', 'Started', 'Completed'))

    tournament_round = models.ForeignKey(TournamentRound)
    started = models.DateTimeField()
    ended = models.DateTimeField()
    team_white = models.ForeignKey(Club, related_name='match_white')
    team_black = models.ForeignKey(Club, related_name='match_black')
    status = models.PositiveIntegerField(choices=STATUSES, default=PENDING)
    #synced = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Matches'

    def __unicode__(self):
        return '{} vs {}'.format(self.team_white, self.team_black)

    @property
    def score(self):
        white_score = Game.objects.filter(match=self).aggregate(
            Sum('white_score'))['white_score__sum'] or 0
        black_score = Game.objects.filter(match=self).aggregate(
            Sum('black_score'))['black_score__sum'] or 0
        return '{} - {}'.format(white_score, black_score)


class Game(models.Model):
    match = models.ForeignKey(Match)
    white = models.ForeignKey(Member, related_name='game_white')
    black = models.ForeignKey(Member, related_name='game_black')
    white_score = models.PositiveIntegerField(default=0)
    black_score = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    synced = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} vs {}'.format(self.white.handle, self.black.handle)

    @property
    def score(self):
        return '{} - {}'.format(self.white_score, self.black_score)
