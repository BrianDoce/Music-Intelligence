With tracks AS
(SELECT

    payload:artist_id::STRING AS artist_id,
    payload:album_id::STRING AS album_id,

    track.value:id::STRING AS track_id,
    track.value:name::STRING AS track_name,

    track.value:track_number::INTEGER AS track_number,
    track.value:disc_number::INTEGER AS disc_number,

    ROUND(track.value:duration_ms::INTEGER / 60000.0, 2) AS duration_mins,

    track.value:explicit::BOOLEAN AS explicit,

    track.value:external_urls.spotify::STRING AS spotify_url,

    track.value:uri::STRING AS spotify_uri,
    track.value:artists[0]:id::STRING AS primary_artist_id,

    ingestion_timestamp,
    current_timestamp() AS dbt_ingestion_timestamp,


    ROW_NUMBER() OVER(
        PARTITION BY track.value:id::STRING
        ORDER BY ingestion_timestamp DESC
    ) AS rn


FROM {{ source('bronze','bronze_tracks') }},
LATERAL FLATTEN(input => payload:data) track
)

SELECT artist_id,
    album_id,
    track_id,
    track_name,
    track_number,
    disc_number,
    duration_ms,
    explicit,
    spotify_url,
    spotify_uri,
    primary_artist_id,
    ingestion_timestamp,
    CURRENT_TIMESTAMP() AS dbt_loaded_at
FROM tracks
WHERE rn = 1