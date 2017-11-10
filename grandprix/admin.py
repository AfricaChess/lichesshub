from django.contrib import admin

from grandprix.models import Tournament, Player, PlayerScore, TournamentType,\
    Season, Points


class PointInline(admin.TabularInline):
    model = Points


@admin.register(TournamentType)
class TournamentTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [PointInline]


@admin.register(Points)
class PointAdmin(admin.ModelAdmin):
    list_display = ['placement', 'points', 'tournament_type']


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'end_date']


@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'kind', 'season', 'date', 'synced', 'error']
    date_heirarchy = ['date']
    list_filter = ['synced', 'error', 'kind']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['name', 'score']


@admin.register(PlayerScore)
class PlayerScoreAdmin(admin.ModelAdmin):
    list_display = ['player', 'tournament', 'rank', 'points']
    list_filter = ['tournament']
