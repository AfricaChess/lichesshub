from django.contrib import admin

from tournament.models import Tournament, TournamentRound, Match, Game


class RoundInline(admin.StackedInline):
    model = TournamentRound


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [RoundInline]


class MatchInline(admin.TabularInline):
    model = Match


@admin.register(TournamentRound)
class TournamentRoundAdmin(admin.ModelAdmin):
    list_display = ['tag', 'tournament']
    inlines = [MatchInline]


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['tournament_round', 'team_white', 'team_black',
                    'started', 'score', 'status']
    list_filter = ['tournament_round', 'tournament_round__tournament']


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['match', 'white', 'black', 'comment', 'score', 'synced', 'error']
