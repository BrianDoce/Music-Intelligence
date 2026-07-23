SELECT
    {{ dbt_utils.generate_surrogate_key(['artist_id']) }} AS artist_key,
    artist_id, 
    artist_name,
    followers,
    popularity
FROM {{ ref('stg_artists')}}