from django import forms

from account.models import Account


class PaymentForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=Account.objects.all())
    amount = forms.DecimalField(max_digits=10, decimal_places=2)

    def __init__(self, balance, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.balance = balance

    def clean_amount(self):
        #import pdb;pdb.set_trace()
        if 'amount' in self.cleaned_data:
            amount = self.cleaned_data['amount']
            if amount > self.balance:
                raise forms.ValidationError("You don't have enough balance")
            return amount


class GameForm(forms.Form):
    pass
