from django.shortcuts import render, get_object_or_404, redirect

from tournament.models import Tournament, Participant
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
    return redirect('tournament_register', id=tournament_id)


def pairings(request, id):
    tourney = get_object_or_404(Tournament, pk=id)
    return render(request, 'tournament/pairings.html', {'tourney': tourney})
