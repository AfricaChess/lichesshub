from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required

from tournament.models import Tournament, Participant, Game, TournamentRound
from player.models import Player
#from tournament.forms import PlayerForm


@login_required
def tournament_list(request):
    tourneys = Tournament.objects.filter(active=True)
    return render(request, 'tournament/list.html', {'tourneys': tourneys})


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
