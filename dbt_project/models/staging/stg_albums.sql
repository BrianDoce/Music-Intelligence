WITH albums AS (

SELECT
    payload:artist_id::STRING AS artist_id,

    album.value:id::STRING AS album_id,
    album.value:name::STRING AS album_name,
    album.value:album_type::STRING AS album_type,

    album.value:release_date::STRING AS release_date,
    album.value:release_date_precision::STRING AS release_date_precision,

    album.value:total_tracks::INTEGER AS total_tracks,

    album.value:external_urls.spotify::STRING AS spotify_url,
    album.value:uri::STRING AS spotify_uri,
    album.value:href::STRING AS api_url,

    ingestion_timestamp,

    ROW_NUMBER() OVER(
        PARTITION BY album.value:id::STRING
        ORDER BY ingestion_timestamp DESC
    ) AS rn


FROM {{ source('bronze','bronze_albums') }},

LATERAL FLATTEN(
    input => payload:data
) album


)

SELECT *
FROM albums
WHERE rn = 1