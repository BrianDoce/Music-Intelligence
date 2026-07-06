from datetime import datetime

def get_artist_albums(client, artist_id):
    artist_albums = client.get_artist_albums(artist_id)
    
    seen = set()
    albums = []
    raw_albums = []
    for album in artist_albums:
        if album.get('id') in seen:
            continue
        seen.add(album.get('id'))
        raw_album_info = client.get_album(album.get('id'))
        raw_albums.append(raw_album_info)

        album_info = {
            "artist_id": artist_id,
            "album_id": album.get("id"),
            "album_name": album.get("name"),
            "album_type": album.get("album_type"),
            "release_date": album.get("release_date"),
            "release_date_precision": album.get("release_date_precision"),
            "total_tracks": album.get("total_tracks"),
            "label": raw_album_info.get("label"),
            "spotify_url": raw_album_info.get("external_urls", {}).get("spotify"),
            "ingestion_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        albums.append(album_info)
    
    return albums, raw_albums