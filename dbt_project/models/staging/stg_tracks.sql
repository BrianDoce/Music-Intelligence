SELECT
    payload:artist_id::STRING AS artist_id,
    payload:album_id::STRING AS album_id,

    track.value:id::STRING AS track_id,
    track.value:name::STRING AS track_name,
    track.value:track_number::INTEGER AS track_number,
    track.value:disc_number::INTEGER AS disc_number,
    track.value:duration_ms::INTEGER AS duration_ms,
    track.value:explicit::BOOLEAN AS explicit,
    track.value:preview_url::STRING AS preview_url,
    track.value:external_urls.spotify::STRING AS spotify_url,
    track.value:uri::STRING AS spotify_uri,

    ingestion_timestamp

FROM {{ source('bronze', 'bronze_tracks') }},
LATERAL FLATTEN(input => payload:data) track