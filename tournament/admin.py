from django.contrib import admin
from django.contrib import messages
from django.conf import settings

from pairing.utils import Pairing
from player.models import Player
from tournament.models import TournamentType, Season, Points, Tournament,\
    TournamentRound, Match, Game, Participant


class RoundInline(admin.StackedInline):
    model = TournamentRound


class PointInline(admin.TabularInline):
    model = Points


@admin.register(TournamentType)
class TournamentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'pairing_type']
    inlines = [PointInline]


@admin.register(Points)
class PointAdmin(admin.ModelAdmin):
    list_display = ['placement', 'points', 'tournament_type']
    list_filter = ['tournament_type', ]


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['player', 'tournament', 'score']
    list_filter = ['tournament']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'kind', 'season', 'active',
                    'synced', 'error']
    inlines = [RoundInline]


class MatchInline(admin.TabularInline):
    model = Match


@admin.register(TournamentRound)
class TournamentRoundAdmin(admin.ModelAdmin):
    list_display = ['tag', 'tournament', 'games', 'paired', 'completed']
    inlines = [MatchInline]
    list_filter = ['tournament']
    actions = ['run_pairing']

    def run_pairing(self, request, queryset):
        if queryset.count() > 1:
            messages.error(request, 'Please start one round at a time')
            return
        # Check that the previous round games are completed already
        tourney_round = queryset[0]
        tourney = tourney_round.tournament
        history = [(i.white.id, i.black.id) for i in Game.objects.filter(
            tourney_round__tournament=tourney)]
        participants = [
            {'id': i.player.id, 'score': i.score}
            for i in Participant.objects.filter(tournament=tourney)]
        p = Pairing(participants, history=history)
        #import pdb; pdb.set_trace()

        for left, right in p.output:
            white = Player.objects.get(pk=left)
            black = Player.objects.get(pk=right)
            Game.objects.create(
                tourney_round=tourney_round,
                white=white,
                black=black)
        if p.remainder:
            white = Player.objects.get(pk=p.remainder['id'])
            Game.objects.create(
                tourney_round=tourney_round,
                white=white,
                black=None,
                white_score=settings.BYE_SCORE,
                comment='Bye',
                synced=True)

        tourney_round.paired = True
        tourney_round.save()
        messages.info(request, 'Pairings completed')
    run_pairing.short_description = 'Run Pairings'


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament_round', 'team_white', 'team_black',
                    'started', 'score', 'status']
    list_filter = ['tournament_round', 'tournament_round__tournament']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['tourney_round', 'white', 'black', 'comment',
                    'score', 'synced', 'error']
    list_filter = ['tourney_round__tournament']
