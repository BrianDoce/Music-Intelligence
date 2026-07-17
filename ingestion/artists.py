from datetime import datetime
def get_artist_info(client, artist_id):
    raw_response = client.get_artist_info(artist_id)

    raw_artist_info = {
        "source": "spotify",
        "endpoint": f"/artists/{artist_id}",
        "ingestion_timestamp": datetime.now().isoformat(),
        "data": raw_response
    }

    artist = {
        'artist_id': raw_response.get('id'),
        'artist_name': raw_response.get('name'),
        'followers': raw_response.get('followers', {}).get('total'),
        'genres': raw_response.get('genres'),
        'popularity': raw_response.get('popularity'),
        'ingestion_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return artist, raw_artist_info

    

    