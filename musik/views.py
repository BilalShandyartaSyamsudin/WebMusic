from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .models import Song, Playlist
from .forms import PlaylistForm, AddToPlaylistForm

def index(request):
    allSongs = Song.objects.all().order_by('-last_updated')
    addToPlaylistForm = AddToPlaylistForm()
    allPlaylists = Playlist.objects.all()
    return render(request, template_name="music/index.html", context={"allSongs" : allSongs, "allPlaylists": allPlaylists, "addToPlaylistForm" : addToPlaylistForm})


def search_songs(request): 
    template_path = 'music/search_result.html'
    
    search_query = request.GET.get('search', None)

    if search_query: 
        search_result = Song.objects.filter(
            Q(songName__icontains=search_query) | 
            Q(album__albumName__icontains=search_query) | 
            Q(album__artist__artistName__icontains=search_query)
        ).distinct()
    else: 
        search_result = Song.objects.all()
        
    context = {'search_result' : search_result, 'search_query' : search_query}
    return render(request, template_path, context)

def add_to_playlist(request, song_id):
    song = get_object_or_404(Song, pk=song_id)

    if request.method == 'POST':
        form = AddToPlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.cleaned_data['playlist']
            playlist.songs.add(song)
            return redirect('index')
        else:
            return JsonResponse({'status': 'error', 'message': 'Formulir tidak valid.'})
    else:
        form = AddToPlaylistForm()

    return render(request, 'music/add_to_playlist.html', {'form': form, 'song': song})

def create_playlist(request):
    form = PlaylistForm() 

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            playlist = form.save()
            return redirect('playlist_detail', playlist_id=playlist.id)

    return render(request, 'music/create_playlist.html', {'form': form})

def playlist_list(request):
    playlists = Playlist.objects.all()
    return render(request, 'music/playlist_list.html', {'playlists': playlists})

def playlist_detail(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    songs = playlist.songs.all()
    return render(request, 'music/playlist_detail.html', {'playlist': playlist, 'songs': songs})

def remove_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    song = get_object_or_404(Song, pk=song_id)

    if request.method == 'POST':
        playlist.songs.remove(song)
        return redirect('playlist_detail', playlist_id=playlist_id)
    else:
        return JsonResponse({'status': 'error', 'message': 'Metode tidak valid untuk penghapusan lagu.'})
    
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    if request.method == 'POST':
        playlist.delete()
        return redirect('playlist_list')
    else:
        return JsonResponse({'status': 'error', 'message': 'Metode tidak valid untuk penghapusan playlist.'})