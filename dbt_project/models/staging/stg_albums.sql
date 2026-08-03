WITH albums_raw AS (

SELECT
    payload:artist_id::STRING AS artist_id,

    album.value:id::STRING AS album_id,
    album.value:name::STRING AS album_name,
    album.value:album_type::STRING AS album_type,

    album.value:release_date::STRING AS raw_release_date,
    album.value:release_date_precision::STRING AS release_date_precision,

    album.value:total_tracks::INTEGER AS total_tracks,

    album.value:external_urls.spotify::STRING AS spotify_url,
    album.value:uri::STRING AS spotify_uri,
    album.value:href::STRING AS spotify_api_url,

    ingestion_timestamp,

    ROW_NUMBER() OVER(
        PARTITION BY album.value:id::STRING
        ORDER BY ingestion_timestamp DESC
    ) AS rn

FROM {{ source('bronze','bronze_albums') }},

LATERAL FLATTEN(
    input => payload:data
) album

),

albums_clean AS (

SELECT
    *,
    CASE
        WHEN release_date_precision = 'day'
            THEN TO_DATE(raw_release_date)

        WHEN release_date_precision = 'month'
            THEN TO_DATE(raw_release_date || '-01')

        WHEN release_date_precision = 'year'
            THEN TO_DATE(raw_release_date || '-01-01')

    END AS release_date

FROM albums_raw

)

SELECT
    artist_id,
    album_id,
    album_name,
    album_type,

    raw_release_date,
    release_date_precision,
    release_date,

    YEAR(release_date) AS release_year,

    total_tracks,

    spotify_url,
    spotify_uri,
    spotify_api_url,

    ingestion_timestamp,
    CURRENT_TIMESTAMP() AS dbt_loaded_at

FROM albums_clean
WHERE rn = 1