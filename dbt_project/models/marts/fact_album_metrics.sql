SELECT
    albums.album_key,
    albums.artist_key,
    albums.release_date_key,

    COUNT(tracks.track_id) AS track_count,

    AVG(tracks.duration_mins) AS avg_track_duration,

    SUM(tracks.duration_mins) AS total_album_duration,

    SUM(IFF(tracks.explicit,1,0)) AS explicit_count,

    SUM(IFF(tracks.explicit,1,0))
    /
    COUNT(tracks.track_id)::FLOAT AS explicit_percentage

FROM {{ ref('dim_albums')}} AS albums

JOIN {{ ref('dim_tracks')}} AS tracks
ON albums.album_key = tracks.album_key

GROUP BY
    albums.album_key,
    albums.artist_key,
    albums.release_date_key