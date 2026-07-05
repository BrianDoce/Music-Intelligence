import requests
import pandas as pd
import os
import json
import api.SpotifyClient as sc
    
data = pd.read_csv('../data/tracked_artists.csv', header=0)
info = {}
spotify_client = sc.SpotifyClient()
albums = []

for index, row in data.iterrows():
    artist_id = row['artist_id']
    artist_info = spotify_client.get_artist_info(artist_id)
    info['artist_id'] = artist_info['id'] if 'id' in artist_info else None
    info['followers'] = artist_info['followers']['total'] if 'followers' in artist_info else None
    info['genres'] = artist_info['genres'] if 'genres' in artist_info else None
    info['popularity'] = artist_info['popularity'] if 'popularity' in artist_info else None

    artist_albums = spotify_client.get_artist_albums(artist_id)
    for album in artist_albums['items']:
        album_info = spotify_client.get_album(album['id'])
        albums.append({
            'artist_id': artist_id,
            'album_id': album_info['id'] if 'id' in album_info else None,
            'album_name': album_info['name'] if 'name' in album_info else None,
            'release_date': album_info['release_date'] if 'release_date' in album_info else None,
            'total_tracks': album_info['total_tracks'] if 'total_tracks' in album_info else None,
            'available_markets': album_info['available_markets'] if 'available_markets' in album_info else None,
            'genres': album_info['genres'] if 'genres' in album_info else None,
            'label': album_info['label'] if 'label' in album_info else None,
        })

    