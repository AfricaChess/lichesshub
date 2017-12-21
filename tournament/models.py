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
    started = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def current_round(self):
        rnds = TournamentRound.objects.filter(tournament=self).order_by('tag')
        unplayed = rnds.filter(completed=False)
        if unplayed:
            return unplayed[0]
        else:
            # Return last round anyway
            last_index = rnds.count() - 1
            return rnds[last_index]

    def compute_scores(self):
        participants = Participant.objects.filter(tournament=self)
        scores = sorted(participants, key=lambda x: x.score, reverse=True)
        points = Points.objects.filter(tournament_type=self.kind).order_by(
            'placement')
        counter = 1
        for pt, participant in zip(points, scores):
            participant.rank = counter,
            participant.points = pt.points
            participant.save()
            counter += 1


class TournamentRound(models.Model):
    tournament = models.ForeignKey(Tournament)
    tag = models.PositiveIntegerField()
    completed = models.BooleanField(default=False)
    paired = models.BooleanField(default=False)

    def __unicode__(self):
        return '{} ({})'.format(self.tournament.name, self.tag)

    @property
    def games(self):
        return Game.objects.filter(tourney_round=self).count()

    class Meta:
        unique_together = ('tournament', 'tag')


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
    black = models.ForeignKey(Player, related_name='game_black', null=True)
    white_score = models.PositiveIntegerField(default=0)
    black_score = models.PositiveIntegerField(default=0)
    comment = models.TextField(blank=True)
    synced = models.BooleanField(default=False)
    error = models.BooleanField(default=False)

    def __unicode__(self):
        _black = self.black.handle if self.black else 'Bye'
        return '{} vs {}'.format(self.white.handle, _black)

    @property
    def score(self):
        return '{} - {}'.format(self.white_score, self.black_score)

    @property
    def white_standing(self):
        participant = Participant.objects.get(
            player=self.white, tournament=self.tourney_round.tournament)
        return participant.score

    @property
    def black_standing(self):
        if not self.black:
            return 0
        participant = Participant.objects.get(
            player=self.black, tournament=self.tourney_round.tournament)
        return participant.score


class Participant(models.Model):
    player = models.ForeignKey(Player)
    tournament = models.ForeignKey(Tournament)
    rank = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return unicode(self.player)

    @property
    def score(self):
        if self.tournament.kind == TournamentType.AUTO:
            return self.points

        white_score = Game.objects.filter(
            tourney_round__tournament=self.tournament,
            white=self.player).aggregate(
            Sum('white_score'))['white_score__sum'] or 0
        black_score = Game.objects.filter(
            tourney_round__tournament=self.tournament,
            black=self.player).aggregate(
            Sum('black_score'))['black_score__sum'] or 0
        return white_score + black_score
