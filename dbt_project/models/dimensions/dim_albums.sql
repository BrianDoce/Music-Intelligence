SELECT
    {{ dbt_utils.generate_surrogate_key(['album_id']) }} AS album_key,
    album_id,
    {{ dbt_utils.generate_surrogate_key(['release_date']) }} AS release_date_key,
    {{ dbt_utils.generate_surrogate_key(['artist_id']) }} AS artist_key,
    album_name,
    album_type
FROM {{ ref('stg_albums') }}