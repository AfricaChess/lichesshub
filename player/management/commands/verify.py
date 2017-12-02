import requests
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from player.models import Player


class Command(BaseCommand):
    help = 'Verify players from lichess.org'

    def handle(self, *args, **kwargs):
        for player in Player.objects.filter(verified=False):
            self.stdout.write('Verifying player {}'.format(player.handle))
            url = '{}user/{}'.format(settings.LICHESS_API_URL, player.handle)
            self.stdout.write(url)
            resp = requests.get(url)
            if resp.status_code == 200:
                results = json.loads(resp.content)
                player.handle = results['username']
                player.blitz_rating = results['perfs']['blitz']['rating']
                player.verified = True
                player.save()

        self.stdout.write('done')
