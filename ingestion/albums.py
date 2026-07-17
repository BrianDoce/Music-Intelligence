from datetime import datetime

def get_artist_albums(client, artist_id):
    raw_response = client.get_artist_albums(artist_id)

    raw_artist_albums = {
        "source": "spotify",
        "endpoint": f"/artists/{artist_id}/albums",
        "artist_id": artist_id,
        "ingestion_timestamp": datetime.now().isoformat(),
        "data": raw_response
    }
    seen = set()
    albums = []
    for album in raw_response:
        if album.get('id') in seen:
            continue
        seen.add(album.get('id'))

        album_info = {
            "artist_id": artist_id,
            "album_id": album.get("id"),
            "album_name": album.get("name"),
            "album_type": album.get("album_type"),
            "release_date": album.get("release_date"),
            "release_date_precision": album.get("release_date_precision"),
            "total_tracks": album.get("total_tracks"),
            "spotify_url": album.get("external_urls", {}).get("spotify"),
            "ingestion_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        albums.append(album_info)
    
    return albums, raw_artist_albums