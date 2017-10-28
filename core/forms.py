from django import forms
from django.contrib.auth.models import User

from account.models import Account


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
    pwd1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    pwd2 = forms.CharField(max_length=50, widget=forms.PasswordInput())

    class Meta:
        model = Account
        fields = ['name', 'email', 'phone']

    def clean_email(self):
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
            try:
                User.objects.get(username=email)
            except User.DoesNotExist:
                return email
            else:
                raise forms.ValidationError('The email you are using is already taken')
