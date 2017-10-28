# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.core.urlresolvers import reverse

from core.forms import EmailForm, ChangePwdForm, RegisterForm


@login_required
def home(request):
    return render(
        request,
        'core/home.html',
        {'login': request.user.last_login})


def forgot(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            usr = form.cleaned_data['email']
            token = default_token_generator.make_token(usr)
            host = request.get_host()
            _url = reverse('change_pwd', args=[usr.id])
            reset_link = 'http://{}{}?token={}'.format(host, _url, token)
            msg = 'Someone asked to reset your password. If it was not you, you can ignore this message else use this link to reset your password {}'.format(reset_link)
            try:
                send_mail(
                    'Reset Password',
                    msg,
                    'drug-exchange@everyday.com.ng',
                    [usr.username])
            except:
                return redirect('not_sent')

            # Send email
            return redirect('email_sent')
    else:
        form = EmailForm()
    return render(request, 'core/forgot.html', {'form': form})


def change_pwd(request, id):
    user = get_object_or_404(User, pk=id)
    token = request.GET.get('token')
    if not token:
        messages.error(request, 'Invalid request')
    else:
        is_valid_token = default_token_generator.check_token(user, token)
        if not is_valid_token:
            messages.error(request, 'Invalid request')
    if request.method == 'POST' and token and is_valid_token:
        form = ChangePwdForm(request.POST)
        if form.is_valid():
            pwd = form.cleaned_data['pwd1']
            user.set_password(pwd)
            user.save()
            return redirect('pwd_set')
    else:
        form = ChangePwdForm()
    return render(request, 'core/change_pwd.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            #import pdb;pdb.set_trace()
            pwd = form.cleaned_data.pop('pwd1')
            email = form.cleaned_data['email']
            #referrer = form.cleaned_data['referrer']
            #pharmacy = form.save(commit=False)
            account = form.save(commit=False)
            usr = User.objects.create_user(
                username=email,
                password=pwd,
                first_name=form.cleaned_data['name'])
            account.user = usr
            account.balance = 5000
            account.save()

            messages.success(
                request, 'Welcome to the Blood bank!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})
