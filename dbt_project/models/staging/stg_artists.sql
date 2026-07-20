WITH ranked AS (

SELECT
    payload:data:id::STRING AS artist_id,
    payload:data:name::STRING AS artist_name,
    payload:data:followers.total::INTEGER AS followers,
    payload:data:popularity::INTEGER AS popularity,
    ingestion_timestamp,

    ROW_NUMBER() OVER(
        PARTITION BY payload:data:id
        ORDER BY ingestion_timestamp DESC
    ) AS rn

FROM {{ source('bronze','bronze_artists') }}

)

SELECT *
FROM ranked
WHERE rn = 1