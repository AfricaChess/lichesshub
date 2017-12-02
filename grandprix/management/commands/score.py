import requests
import json
import time

from django.core.management.base import BaseCommand
# from django.conf import settings

from grandprix.models import Tournament, TournamentType, Player, PlayerScore,\
    Points


class Command(BaseCommand):
    help = 'Get tournament result and save for each player'

    def handle(self, *args, **kwargs):
        tourneys = Tournament.objects.filter(
            synced=False, error=False, kind__pairing_type=TournamentType.AUTO)
        for tourney in tourneys:
            points = Points.objects.filter(tournament_type=tourney.kind)

            time.sleep(2)
            url = 'https://lichess.org/api/tournament/{}'.format(tourney.name)
            self.stdout.write(url)
            resp = requests.get(url)
            data = json.loads(resp.content)
            finished = data.get('isFinished', False)
            if resp.status_code == 200 and finished:
                content = data['standing']['players']
                top_ten = {i['rank']: i['name'] for i in content}
                self.stdout.write(str(top_ten))
                for item in content:
                    try:
                        pts = points.get(placement=item['rank'])
                    except Points.DoesNotExist:
                        continue
                    else:
                        player, _ = Player.objects.get_or_create(
                            name=item['name'],
                            tournament_type=tourney.kind)
                        PlayerScore.objects.create(
                            player=player,
                            tournament=tourney,
                            rank=item['rank'],
                            points=pts.points)

                tourney.synced = True
                tourney.save()
        self.stdout.write('done')
