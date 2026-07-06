from datetime import datetime

def get_artist_albums(client, artist_id):
    artist_albums = client.get_artist_albums(artist_id)
    
    albums = []
    raw_albums = []
    for album in artist_albums['items']:
        raw_album_info = client.get_album(album.get('id'))
        raw_albums.append(raw_album_info)

        album_info = {
            'artist_id': artist_id,
            'album_id': album.get('id'),
            'album_name': album.get('name'),
            'release_date': album.get('release_date'),
            'total_tracks': album.get('total_tracks'),
            'available_markets': album.get('available_markets'),
            'genres': raw_album_info.get('genres'),
            'label': raw_album_info.get('label'),
            'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        albums.append(album_info)
    
    return albums, raw_albums