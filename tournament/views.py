from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings

from tournament.models import Tournament, Participant, Game, TournamentRound
from player.models import Player
from tournament.forms import PlayerForm


def tournament_list(request):
    tourneys = Tournament.objects.filter(active=True)
    return render(request, 'tournament/list.html', {'tourneys': tourneys})


def register(request, id):
    tourney = get_object_or_404(Tournament, pk=id)
    if request.method == 'POST':
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.cleaned_data['handle']
            Participant.objects.get_or_create(player=player, tournament=tourney)
    else:
        form = PlayerForm()
    parts = [i.player for i in Participant.objects.filter(tournament=tourney)]
    non_parts = [i for i in Player.objects.order_by('handle') if i not in parts]
    return render(
        request,
        'tournament/register.html',
        {
            'tourney': tourney,
            'participants': parts,
            'non_participants': non_parts,
            'form': form
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
