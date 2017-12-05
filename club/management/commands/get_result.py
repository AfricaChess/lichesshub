import requests
import time

from django.core.management.base import BaseCommand
from django.conf import settings

from tournament.models import Game


class Command(BaseCommand):
    help = 'Get Result of game'

    def handle(self, *args, **kwargs):
        games = Game.objects.filter(
            synced=False, error=False, game_id__isnull=False)
        for game in games:
            url = '{}game/{}'.format(settings.LICHESS_API_URL, game.game_id)
            self.stdout.write(url)
            resp = requests.get(url)
            data = resp.json()

            # TODO: Verify that the user IDs are correct
            if resp.status_code == 200:
                if data['status'] == 'draw':
                    game.white_score = 1
                    game.black_score = 1
                else:
                    if data['winner'] == 'white':
                        game.white_score = 2
                        game.black_score = 0
                    else:
                        game.white_score = 0
                        game.black_score = 2
                game.synced = True
                game.comment = '{} vs {}'.format(
                    data['players']['white']['userId'], data['players']['black']['userId'])
                game.save()
                time.sleep(5)
            else:
                game.error = True
                game.save()
                time.sleep(65)

            #import pdb;pdb.set_trace()
            #results = resp.content['paginator']['currentPageResults']
            self.stdout.write('done')
