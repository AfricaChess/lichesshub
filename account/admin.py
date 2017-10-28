# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from account.models import Account, Transaction


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'balance', 'registered_on']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'kind', 'amount', 'balance',
                    'trans_date', 'processed']
