from django.contrib import admin

from club.models import Club, Member


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['handle', 'blitz_rating', 'order', 'club']
    list_filter = ['club']
