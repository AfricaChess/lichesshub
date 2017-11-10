import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models.aggregates import Max
from django.db.models import Q
from django.utils import timezone

from club.models import Club, Member
from club.forms import MemberForm
from tournament.models import Match, Game
from grandprix.models import Player


def json_bad_request(error):
    out = {'success': 'false'}
    out.update({'error': error})
    return HttpResponseBadRequest(json.dumps(out))


def grandprix(request):
    leaderboard = [
        {
            'score': i['score'],
            'name': i['name'],
            'position': idx + 1
        }
        for idx, i in enumerate(get_leaderboard())]
    #import pdb;pdb.set_trace()
    return render(request, 'club/grandprix.html', {'leaderboard': leaderboard})


@login_required
def profile(request):
    clubs = Club.objects.filter(captain=request.user)
    if clubs:
        clb = clubs[0]
        return render(request, 'club/profile.html', {'club': clb})
    else:
        return redirect('login')
    #try:
    #    clb = Club.objects.get(captain=request.user)
    #except Club.DoesNotExist:
    #    return redirect('login')
    #else:
    #    return render(request, 'club/profile.html', {'club': clb})


def get_members(clb):
    return [
        {
            'id': member.id,
            'handle': member.handle,
            'order': member.order,
            'rating': member.blitz_rating
        } for member in Member.objects.filter(club=clb).order_by('order')]


def arrange_boards(white_team, black_team):
    out = []
    for i in range(len(white_team)):
        if i % 2:
            out.append({'white': black_team[i].handle, 'black': white_team[i].handle})
        else:
            out.append({'white': white_team[i].handle, 'black': black_team[i].handle})
    return out


def get_matches(clb):
    today = timezone.now().date()
    #import pdb;pdb.set_trace()
    matches = Match.objects.filter(started__date=today).filter(
        Q(team_white=clb) | Q(team_black=clb))
    out = []
    for match in matches:
        white = match.team_white
        black = match.team_black
        top_white = Member.objects.filter(club=white).order_by('order')[:4]
        top_black = Member.objects.filter(club=black).order_by('order')[:4]
        match_dict = {
            'white_team': white.name,
            'black_team': black.name,
            'white_members': [
                {
                    'handle': w.handle,
                    'rating': w.blitz_rating
                } for w in top_white],
            'black_members': [
                {
                    'handle': b.handle,
                    'rating': b.blitz_rating
                } for b in top_black],
            'board_order': arrange_boards(top_white, top_black),
            'status': match.status,
            'id': match.id
        }
        out.append(match_dict)
    return out


def get_leaderboard():
    players = [
        {
            'name': player.name,
            'score': player.score
        } for player in Player.objects.all()
    ]
    players.sort(key=lambda x: x['score'], reverse=True)
    return players


@login_required
def leaderboard(request):
    return JsonResponse({'leaderboard': get_leaderboard()})


@login_required
def info(request):
    clb = Club.objects.get(captain=request.user)
    members = get_members(clb)
    matches = get_matches(clb)
    leaderboard = get_leaderboard()
    return JsonResponse(
        {
            'members': members,
            'club': clb.name,
            'matches': matches,
            'leaderboard': leaderboard
        })


@login_required
def save_order(request):
    clb = Club.objects.get(captain=request.user)
    new_order = request.GET.get('order').split('|')
    for idx, handle in enumerate(new_order):
        try:
            member = Member.objects.get(club=clb, handle=handle)
        except Member.DoesNotExist:
            continue
        else:
            member.order = idx + 1
            member.save()
    return JsonResponse({})


@csrf_exempt
@login_required
def add_member(request):
    clb = Club.objects.get(captain=request.user)
    #import pdb;pdb.set_trace()
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            max_order = Member.objects.aggregate(Max('order'))['order__max'] or 0
            new_order = max_order + 1
            Member.objects.create(
                club=clb, handle=form.cleaned_data['handle'], order=new_order)
            members = get_members(clb)
            return JsonResponse({'members': members})
        else:
            res = form.errors['handle'][0]
            print res
    return json_bad_request(res)


@csrf_exempt
@login_required
def remove_member(request, id):
    clb = Club.objects.get(captain=request.user)
    member = get_object_or_404(Member, pk=id)
    member.delete()
    members = get_members(clb)
    return JsonResponse({'members': members})


@login_required
def cancel_match(request, id):
    clb = get_object_or_404(Club, captain=request.user)
    match = get_object_or_404(Match, pk=id)
    match.status = Match.PENDING
    match.save()
    members = get_members(clb)
    matches = get_matches(clb)
    return JsonResponse(
        {'members': members, 'club': clb.name, 'matches': matches})


@login_required
def start_match(request, id):
    clb = get_object_or_404(Club, captain=request.user)
    match = get_object_or_404(Match, pk=id)
    match.status = Match.STARTED
    match.started = timezone.now()
    match.save()
    members = get_members(clb)
    matches = get_matches(clb)
    return JsonResponse(
        {'members': members, 'club': clb.name, 'matches': matches})


@login_required
def complete_match(request, id):
    clb = get_object_or_404(Club, captain=request.user)
    match = get_object_or_404(Match, pk=id)
    match.status = Match.COMPLETED
    match.ended = timezone.now()
    match.save()
    # Save game
    top_white = Member.objects.filter(club=match.team_white).order_by('order')[:4]
    top_black = Member.objects.filter(club=match.team_black).order_by('order')[:4]
    for i in range(4):
        Game.objects.get_or_create(match=match, white=top_white[i], black=top_black[i])
        Game.objects.get_or_create(match=match, white=top_black[i], black=top_white[i])

    members = get_members(clb)
    matches = get_matches(clb)
    return JsonResponse(
        {'members': members, 'club': clb.name, 'matches': matches})
