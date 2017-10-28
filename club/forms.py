from django import forms

from club.models import Member


class MemberForm(forms.Form):
    handle = forms.CharField(max_length=100)

    def clean_handle(self):
        try:
            Member.objects.get(handle=self.cleaned_data['handle'])
        except Member.DoesNotExist:
            return self.cleaned_data['handle']
        raise forms.ValidationError('This handle already exists')
