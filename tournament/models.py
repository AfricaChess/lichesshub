from __future__ import unicode_literals

from django.db import models
from django.db.models.aggregates import Sum
from django.utils import timezone

from club.models import Club
from player.models import Player


class TournamentType(models.Model):
    AUTO = 0
    MANUAL = 1
    ROUND_ROBIN = 2
    SWISS = 3
    PAIRINGS = enumerate(('Auto', 'Manual', 'Round Robin', 'Swiss'))
    name = models.CharField(max_length=50)
    pairing_type = models.PositiveIntegerField(choices=PAIRINGS, default=AUTO)

    def __unicode__(self):
        return self.name


class Season(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()

    def __unicode__(self):
        return self.name


class Points(models.Model):
    placement = models.PositiveIntegerField()
    points = models.PositiveIntegerField()
    tournament_type = models.ForeignKey(TournamentType)

    def __unicode__(self):
        return '{}'.format(self.placement)

    class Meta:
        verbose_name_plural = 'Points'


class Tournament(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    synced = models.BooleanField(default=False)
    error = models.BooleanField(default=False)
    kind = models.ForeignKey(TournamentType, null=True)
    season = models.ForeignKey(Season, null=True)
    active = models.BooleanField(default=True)

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
    match = models.ForeignKey(Match, null=True, blank=True)
    tourney_round = models.ForeignKey(TournamentRound, null=True, blank=True)
    game_id = models.CharField(max_length=50, null=True, blank=True)
    white = models.ForeignKey(Player, related_name='game_white')
    black = models.ForeignKey(Player, related_name='game_black')
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


class Participant(models.Model):
    player = models.ForeignKey(Player)
    tournament = models.ForeignKey(Tournament)

    def __unicode__(self):
        return unicode(self.player)
