from django.contrib import admin

from grandprix.models import Tournament, Player, PlayerScore


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'date', 'synced', 'error']
    date_heirarchy = ['date']
    list_filter = ['synced', 'error']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'score']


@admin.register(PlayerScore)
class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ['player', 'tournament', 'rank', 'points']
