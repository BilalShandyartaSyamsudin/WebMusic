from django import forms
from .models import Playlist

class AddToPlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(queryset=Playlist.objects.all(), empty_label=None)
    
class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name']