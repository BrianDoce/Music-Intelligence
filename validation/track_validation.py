def track_validation(track):
    required_fields = [
        "track_id",
        "track_name",
        "album_id",
        "track_number",
        "duration_ms",
        "explicit",
        "ingestion_timestamp"
    ]

    return all(track.get(field) is not None for field in required_fields)