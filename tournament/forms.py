from django import forms

from player.models import Player


class PlayerForm(forms.Form):
    handle = forms.CharField(max_length=100)

    def clean_handle(self):
        if 'handle' in self.cleaned_data:
            _handle = self.cleaned_data['handle']
            try:
                _player = Player.objects.get(handle__iexact=_handle)
            except Player.DoesNotExist:
                return Player.objects.create(
                    handle=_handle, verified=False, blitz_rating=0)
            else:
                return _player
