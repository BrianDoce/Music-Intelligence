from datetime import datetime
def get_tracks(client, artist_id,album_id):
    raw_response = client.get_album_tracks(album_id)

    raw_track_info = {
        "source": "spotify",
        "endpoint": f"/albums/{album_id}/tracks",
        "artist_id": artist_id,
        "album_id": album_id,
        "ingestion_timestamp": datetime.now().isoformat(),
        "data": raw_response
    }

    track_records = []
    for track in raw_response:
        track_record = {
            "track_id": track.get("id"),
            "track_name": track.get("name"),
            "album_id": album_id,

            "track_number": track.get("track_number"),
            "disc_number": track.get("disc_number"),

            "duration_ms": track.get("duration_ms"),
            "explicit": track.get("explicit"),

            "preview_url": track.get("preview_url"),

            "spotify_url": track.get("external_urls", {}).get("spotify"),

            "uri": track.get("uri"),

            "ingestion_timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        track_records.append(track_record)

    return track_records, raw_track_info