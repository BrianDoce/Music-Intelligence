WITH album_stats AS (

SELECT
    album_key,
    artist_key,
    COUNT(track_id) AS track_count,
    AVG(duration_mins) AS avg_track_duration,
    SUM(duration_mins) AS album_duration_mins,
    SUM(IFF(explicit,1,0)) AS explicit_tracks

FROM {{ ref('dim_tracks') }}

GROUP BY
    album_key,
    artist_key

)

SELECT
    a.artist_key,

    COUNT(DISTINCT album_key) AS album_count,

    SUM(track_count) AS track_count,

    AVG(track_count) AS avg_tracks_per_album,

    AVG(avg_track_duration) AS avg_track_duration,

    AVG(album_duration_mins) AS avg_album_duration,

    SUM(explicit_tracks) AS explicit_track_count

FROM album_stats a

JOIN {{ ref('dim_artists') }} ar
ON a.artist_key = ar.artist_key

GROUP BY
    a.artist_key