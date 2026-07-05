from datetime import datetime
def get_artist_info(client, artist_id):
    artist_info = client.get_artist_info(artist_id)

    artists = {
        'artist_id': artist_info.get('id'),
        'artist_name': artist_info.get('name'),
        'followers': artist_info.get('followers', {}).get('total'),
        'genres': artist_info.get('genres'),
        'popularity': artist_info.get('popularity'),
        'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return artists, artist_info

    

    