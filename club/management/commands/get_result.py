import requests
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from tournament.models import Game


class Command(BaseCommand):
    help = 'Get Result of game'

    def handle(self, *args, **kwargs):
        games = Game.objects.filter(synced=False, error=False)
        if not games:
            self.stderr.write('No games to check')
        else:
            game = games[0]
            url = '{}games/vs/{}/{}'.format(
                settings.LICHESS_API_URL, game.white.handle, game.black.handle)
            self.stdout.write(url)
            resp = requests.get(url)
            results = json.loads(resp.content)['currentPageResults']

            #import pdb;pdb.set_trace()
            for res in results:
                if res['players']['white']['userId'] == game.white.handle and res['players']['black']['userId'] == game.black.handle:
                    if res['status'] == 'draw':
                        game.white_score = 1
                        game.black_score = 1
                    else:
                        if res['winner'] == 'white':
                            game.white_score = 2
                            game.black_score = 0
                        else:
                            game.white_score = 0
                            game.black_score = 2
                    game.synced = True
                    game.save()
                    break
            else:
                game.error = True
                game.save()

            #import pdb;pdb.set_trace()
            #results = resp.content['paginator']['currentPageResults']
            self.stdout.write(str(results))
