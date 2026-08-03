WITH album_stats AS (

SELECT

    album_key,

    COUNT(*) AS album_track_count,

    AVG(duration_mins) AS avg_track_duration,

    SUM(duration_mins) AS album_duration_mins,

    SUM(IFF(explicit,1,0)) AS explicit_tracks

FROM {{ ref('dim_tracks') }}

GROUP BY
    album_key

)

SELECT

    al.artist_key,

    MAX(ar.artist_name) AS artist_name,

    MAX(ar.followers) AS followers,

    MAX(ar.popularity) AS popularity,
    
    COUNT(DISTINCT al.album_key) AS album_count,

    SUM(a.album_track_count) AS track_count,

    AVG(a.album_track_count) AS avg_tracks_per_album,

    AVG(a.avg_track_duration) AS avg_track_duration,

    AVG(a.album_duration_mins) AS avg_album_duration,

    SUM(a.explicit_tracks) AS explicit_track_count


FROM album_stats a

JOIN {{ ref('dim_albums') }} al
ON a.album_key = al.album_key

JOIN {{ ref('dim_artists') }} ar
ON al.artist_key = ar.artist_key


GROUP BY

    al.artist_key