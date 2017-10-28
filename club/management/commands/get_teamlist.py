import requests
import json

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from club.models import Club, Member


class Command(BaseCommand):
    help = 'Get List of players from lichess for team'

    def handle(self, *args, **kwargs):
        teams = Club.objects.order_by('last_sync')
        if not teams:
            self.stderr.write('No teams set up')

        team = teams[0]
        team_name = team.name
        self.stdout.write('Getting players for team {}'.format(team_name))
        url = '{}user?team={}&nb=20&page=1'.format(
            settings.LICHESS_API_URL, team_name)
        self.stdout.write(url)
        resp = requests.get(url)
        results = json.loads(resp.content)['paginator']['currentPageResults']
        for player in results:
            try:
                mb = Member.objects.get(handle=player['id'])
            except Member.DoesNotExist:
                Member.objects.create(
                    handle=player['id'],
                    club=team,
                    blitz_rating=player['perfs']['blitz']['rating']
                )
            else:
                mb.blitz_rating = player['perfs']['blitz']['rating']
                mb.club = team
                mb.save()
                self.stdout.write('Saving {}'.format(player['username']))
        # Update last_sync
        team.last_sync = timezone.now()
        team.save()

        #import pdb;pdb.set_trace()
        #results = resp.content['paginator']['currentPageResults']
        self.stdout.write(str(results))
