SELECT
    {{ dbt_utils.generate_surrogate_key(['track_id']) }} AS track_key,
    {{ dbt_utils.generate_surrogate_key(['album_id']) }} AS album_key,
    track_id,
    track_name,
    duration_mins,
    explicit,
    track_number,
    disc_number
FROM {{ ref('stg_tracks') }}