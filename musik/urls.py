
from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('search/', views.search_songs, name='search_songs'),
    path('add_to_playlist/<int:song_id>/', views.add_to_playlist, name='add_to_playlist'),
    path('create_playlist/', views.create_playlist, name='create_playlist'),
    path('playlist/', views.playlist_list, name='playlist_list'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlist/<int:playlist_id>/remove/<int:song_id>/', views.remove_from_playlist, name='remove_from_playlist'),
    path('playlist/remove/<int:playlist_id>/', views.delete_playlist, name='delete_playlist'),
]
