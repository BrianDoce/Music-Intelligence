SELECT
    payload:data:track_id::VARCHAR AS track_id,
    payload:data:track_name::VARCHAR AS track_name,
    payload:data:album_id::VARCHAR AS album_id,
    payload:data:track_number::INTEGER AS track_number,
    payload:data:disc_number::INTEGER AS disc_number,
    payload:data:duration_ms::INTEGER AS duration_ms,
    payload:data:explicit::BOOLEAN AS explicit,
    payload:data:spotify_url::VARCHAR AS spotify_url,
    payload:data:uri::VARCHAR AS spotify_uri,
    payload:data:ingestion_timestamp::TIMESTAMP AS ingestion_timestamp
FROM {{ source('bronze', 'bronze_tracks') }}