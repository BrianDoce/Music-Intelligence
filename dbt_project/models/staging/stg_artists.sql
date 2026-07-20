SELECT
    payload:data:id::VARCHAR AS artist_id,
    payload:data:name::VARCHAR AS artist_name,
    payload:data:followers.total::INTEGER AS artist_followers,
    payload:data:popularity::INTEGER AS artist_popularity,
    ingestion_timestamp
FROM {{ source('bronze', 'bronze_artists')}}