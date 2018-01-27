from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from collections import defaultdict

from tournament.models import Tournament, Participant, Game, TournamentRound,\
    Season, TournamentType
from player.models import Player
from pairing.utils import Pairing
#from tournament.forms import PlayerForm


@login_required
def tournament_list(request):
    tourneys = Tournament.objects.filter(active=True).exclude(
        kind__pairing_type=TournamentType.AUTO)
    return render(
        request,
        'tournament/list.html',
        {'tourneys': tourneys, 'tourney_types': TournamentType.objects.all()})


@login_required
def register(request, id):
    tourney = get_object_or_404(Tournament, pk=id)
    if request.method == 'POST':
        player = Player.objects.get(user=request.user)
        Participant.objects.get_or_create(player=player, tournament=tourney)

    parts = [i.player for i in Participant.objects.filter(tournament=tourney)]
    return render(
        request,
        'tournament/register.html',
        {
            'tourney': tourney,
            'participants': parts,
        }
    )


def join(request, tournament_id, player_id):
    tourney = get_object_or_404(Tournament, pk=tournament_id)
    player = get_object_or_404(Player, pk=player_id)
    Participant.objects.get_or_create(player=player, tournament=tourney)
    # Give bye for every missed round
    for tourney_round in TournamentRound.objects.filter(
            tournament=tourney, paired=True):
        Game.objects.create(
            tourney_round=tourney_round,
            white=player,
            black=None,
            white_score=settings.BYE_SCORE,
            comment='Bye',
            synced=True)
    return redirect('tournament_register', id=tournament_id)


def pairings(request, id):
    tourney = get_object_or_404(Tournament, pk=id)
    tourney_round = tourney.current_round
    games = Game.objects.filter(tourney_round=tourney_round)
    return render(
        request,
        'tournament/pairings.html',
        {
            'tourney': tourney,
            'current_round': tourney_round,
            'games': games
        })


def run_pairings(request, id):
    tourney_round = get_object_or_404(TournamentRound, pk=id)
    tourney = tourney_round.tournament
    history = [(i.white.id, i.black.id) for i in Game.objects.filter(
        tourney_round__tournament=tourney)]
    participants = [
        {'id': i.player.id, 'score': i.score}
        for i in Participant.objects.filter(tournament=tourney)]
    pair = Pairing(participants, history=history)

    for left, right in pair.output:
        white = Player.objects.get(pk=left)
        black = Player.objects.get(pk=right)
        Game.objects.create(
            tourney_round=tourney_round,
            white=white,
            black=black)
    if pair.remainder:
        #import pdb;pdb.set_trace()
        white = Player.objects.get(pk=pair.remainder[0]['id'])
        Game.objects.create(
            tourney_round=tourney_round,
            white=white,
            black=None,
            white_score=settings.BYE_SCORE,
            comment='Bye',
            synced=True)

    tourney_round.paired = True
    tourney_round.save()
    messages.success(request, 'Pairings completed')
    return redirect('tournament_pairings', id=tourney.id)


def leaderboard(request, id):
    tourney_type = get_object_or_404(TournamentType, pk=id)
    now = timezone.now().date()
    season = Season.objects.filter(start_date__lte=now, end_date__gte=now)
    _participants = Participant.objects.filter(
        tournament__kind=tourney_type, tournament__season=season)
    participants = sorted(_participants, key=lambda x: x.score, reverse=True)

    d = defaultdict(list)
    for participant in participants:
        if participant.player.handle:
            if len(d[participant.player.handle]) == 10:
                continue
            else:
                d[participant.player.handle].append(participant.score)

    out = [{'name': key, 'score': sum(val)} for key, val in d.items()]
    #out = [{'name': key, 'score': val} for key, val in d.items()]
    out.sort(key=lambda x: x['score'], reverse=True)
    return render(
        request,
        'tournament/leaderboard.html',
        {'players': out, 'kind': tourney_type})
