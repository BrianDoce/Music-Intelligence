from datetime import datetime
def get_artist_info(client, artist_id):
    raw_artist_info = client.get_artist_info(artist_id)

    artist = {
        'artist_id': raw_artist_info.get('id'),
        'artist_name': raw_artist_info.get('name'),
        'followers': raw_artist_info.get('followers', {}).get('total'),
        'genres': raw_artist_info.get('genres'),
        'popularity': raw_artist_info.get('popularity'),
        'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return artist, raw_artist_info

    

    