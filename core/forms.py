from django import forms
from django.contrib.auth.models import User

#from account.models import Account
from player.models import Player


class EmailForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                usr = User.objects.get(username=email)
            except User.DoesNotExist:
                raise forms.ValidationError(
                    'The email you entered does not exist in our records')
            else:
                return usr


class ChangePwdForm(forms.Form):
    pwd1 = forms.CharField(
        max_length=50, min_length=5, widget=forms.PasswordInput)
    pwd2 = forms.CharField(
        max_length=50, min_length=5, widget=forms.PasswordInput)

    def clean(self):
        if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            if self.cleaned_data['pwd1'] != self.cleaned_data['pwd2']:
                raise forms.ValidationError(
                    'Please enter the same value in both fields')
            return self.cleaned_data


class RegisterForm(forms.ModelForm):
    email = forms.EmailField()
    pwd1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    pwd2 = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = Player
        fields = ['handle']

    def clean(self):
        if 'pwd1' in self.cleaned_data and 'pwd2' in self.cleaned_data:
            if self.cleaned_data['pwd1'] != self.cleaned_data['pwd2']:
                raise forms.ValidationError('The passwords are not alike')
            return self.cleaned_data

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            else:
                raise forms.ValidationError(
                    'The email you are using is already taken')

    def clean_handle(self):
        if 'handle' in self.cleaned_data:
            handle = self.cleaned_data['handle']
            try:
                player = Player.objects.get(handle__iexact=handle)
            except Player.DoesNotExist:
                return handle
            else:
                if player.user:
                    raise forms.ValidationError(
                        'This handle is already registered')
                else:
                    return handle
