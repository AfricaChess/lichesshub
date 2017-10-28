# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz
import json
import requests
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from account.models import Account, Transaction, Game
from account.forms import PaymentForm


def json_bad_request(error):
    out = {'success': 'false'}
    out.update({'error': error})
    return HttpResponseBadRequest(json.dumps(out))


def get_other_accounts(usr):
    return [
        {
            'id': acct.id,
            'name': acct.name,
            'email': acct.email
        } for acct in Account.objects.exclude(user=usr)]


def get_profile(acct):
    return {
        'id': acct.id,
        'name': acct.name,
        'phone': acct.phone,
        'email': acct.email,
        'balance': '{}'.format(acct.balance),
        'regdate': acct.registered_on.strftime('%d %b %Y'),
    }


@login_required
def profile(request):
    try:
        acct = get_object_or_404(Account, user=request.user)
    except Account.DoesNotExist:
        return json_bad_request('Invalid profile')
    else:
        profile = get_profile(acct)
        accounts = get_other_accounts(request.user)
        transactions = get_transactions(acct)
        games = get_games()
        return JsonResponse(
            {
                'profile': profile,
                'accounts': accounts,
                'transactions': transactions,
                'games': games
            })


def get_transactions(acct):
    return [
        {
            'id': trans.id,
            'kind': trans.get_kind_display(),
            'amount': '{}'.format(trans.amount),
            'balance': '{}'.format(trans.balance),
            'comment': trans.comment,
            'processed': trans.processed,
            'when': trans.trans_date.strftime('%d %b %Y %H:%M %p')
        } for trans in Transaction.objects.filter(account=acct).order_by('-id')
    ]


@csrf_exempt
@login_required
def pay(request):
    #import pdb;pdb.set_trace()
    try:
        sender = get_object_or_404(Account, user=request.user)
    except Account.DoesNotExist:
        return json_bad_request('Invalid transaction')
    else:
        if request.method == 'POST':
            form = PaymentForm(sender.balance, request.POST)
            if form.is_valid():
                amount = form.cleaned_data['amount']
                recipient = form.cleaned_data['recipient']
                sender_balance = sender.balance - amount
                recipient_balance = recipient.balance + amount

                Transaction.objects.create(
                    account=sender,
                    kind=Transaction.DEBIT,
                    amount=amount,
                    balance=sender_balance,
                    comment='Sent to {}'.format(recipient.name),
                    processed=True)
                Transaction.objects.create(
                    account=recipient,
                    kind=Transaction.CREDIT,
                    amount=amount,
                    balance=recipient_balance,
                    comment='Received from {}'.format(sender.name),
                    processed=True)

                sender.balance = sender_balance
                sender.save()

                recipient.balance = recipient_balance
                recipient.save()

                transactions = get_transactions(sender)
                profile = get_profile(sender)
                return JsonResponse(
                    {'profile': profile, 'transactions': transactions})
            else:  # Invalid form
                pass
    return json_bad_request('Invalid transaction body')


@csrf_exempt
def save_game(request):
    white = request.POST.get('white')
    black = request.POST.get('black')
    game = Game.objects.create(white=white, black=black)
    games = get_games()
    return JsonResponse({'game': unicode(game), 'games': games})


def get_games():
    return [
        {
            'id': g.id,
            'white': g.white,
            'black': g.black,
            'white_score': g.white_score,
            'black_score': g.black_score,
            'when': g.game_date.strftime('%d %b %Y %H:%M')
        }
        for g in Game.objects.all()]


def get_result(request, id):
    #import pdb;pdb.set_trace()
    game = Game.objects.get(pk=id)
    url = 'https://lichess.org/api/games/vs/{}/{}'.format(
        game.white, game.black)
    res = requests.get(url)
    data = json.loads(res.content)['currentPageResults']
    #fltd = [i for i in data if i['players']['white']['userId'] == game.white
    #        and pytz.timezone('UTC').localize(
    #            datetime.fromtimestamp(i['createdAt']/1000),
    #            is_dst=None) >= game.game_date]
    fltd = [i for i in data if i['players']['white']['userId'] == game.white]
    if fltd:
        last_game = fltd[0]
        if last_game['status'] == 'draw':
            result = {'white': 0.5, 'black': 0.5}
        elif last_game['winner'] == 'white':
            result = {'white': 1, 'black': 0}
        else:
            result = {'white': 0, 'black': 1}
    else:
        result = {'white': None, 'black': None}
    return JsonResponse(result)
