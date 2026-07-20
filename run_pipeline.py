from utils.logger import get_logger
from ingestion.albums import get_artist_albums
from ingestion.artists import get_artist_info
from validation.album_validation import album_validation
from validation.artist_validation import artist_validation
from api.SpotifyClient import SpotifyClient
from utils.savejson import save_json
from utils.s3uploader import export_to_s3
from datetime import datetime
from ingestion.tracks import get_tracks
from validation.track_validation import track_validation
import pandas as pd
import time

def main():
    now = time.time()
    logger = get_logger("spotify_pipeline")
    artist_ids = pd.read_csv("data/tracked_artists.csv")["artist_id"].tolist()
    run_date = datetime.now().strftime("%Y-%m-%d")

    artist_ls = []
    raw_artist_ls = []

    album_ls = []
    raw_album_ls = []

    track_ls = []
    raw_track_ls = [] 

    valid_artists = 0
    invalid_artists = 0

    valid_tracks = 0
    invalid_tracks = 0
    tracks_processed = 0

    valid_albums = 0
    invalid_albums = 0
    albums_processed = 0

    client = SpotifyClient()

    for i, artist_id in enumerate(artist_ids, start=1):
        logger.info(f"Processing artist {i}/{len(artist_ids)}: {artist_id}")
        try:
            artist, raw_artist_info = get_artist_info(client, artist_id)
            
            logger.info(f"Fetching albums for {artist['artist_name']}")

            if artist_validation(artist):
                valid_artists += 1
                artist_ls.append(artist)
                raw_artist_ls.append(raw_artist_info)
                logger.info(f"Artist {artist['artist_name']} validated successfully.")
            else:
                invalid_artists += 1
                logger.warning(f"Artist {artist['artist_name']} failed validation.")
                continue
            
            album_records, raw_album_info = get_artist_albums(client, artist_id)
            raw_album_ls.append(raw_album_info)
            for album in album_records:
                albums_processed += 1
                logger.info(f"Processing album {album['album_name']}")
                if album_validation(album):
                    valid_albums += 1
                    album_ls.append(album)
                    logger.info(f"Album {album['album_name']} validated successfully.")    
                    track_records, raw_track_info = get_tracks(client, artist_id, album['album_id'])

                    raw_track_ls.append(raw_track_info)

                    for track in track_records:
                        logger.info(f"Processing track {track['track_name']} from album {album['album_name']}")
                        tracks_processed += 1

                        if track_validation(track):
                            logger.info(f"Track {track['track_name']} validated successfully.")
                            track_ls.append(track)
                            valid_tracks += 1
                        else:
                            invalid_tracks += 1
                            logger.warning(f"Track {track['track_name']} failed validation.")

                else:
                    invalid_albums += 1
                    logger.warning(f"Album {album['album_name']} failed validation.")
            time.sleep(1)

        except Exception as e:
            logger.error(f"Error processing artist ID {artist_id}: {e}")


    logger.info(f"Artists processed: {len(artist_ids)}")
    logger.info(f"Albums processed: {albums_processed}")
    logger.info(f"Tracks processed: {tracks_processed}")

    logger.info(f"Artists collected: {len(artist_ls)}")
    logger.info(f"Albums collected: {len(album_ls)}")
    logger.info(f"Tracks collected: {len(track_ls)}")

    logger.info(f"Artists validated: {valid_artists}, Invalid artists: {invalid_artists}")
    logger.info(f"Albums validated: {valid_albums}, Invalid albums: {invalid_albums}")
    logger.info(f"Tracks validated: {valid_tracks}, Invalid tracks: {invalid_tracks}")

    artist_success_rate = valid_artists / len(artist_ids) * 100
    album_success_rate = (
        valid_albums / max(albums_processed, 1)
    ) * 100

    track_success_rate = (
    valid_tracks /
    max(tracks_processed, 1)
) * 100
    
    logger.info(f"Artist validation rate: {artist_success_rate:.2f}%")
    logger.info(f"Album validation rate: {album_success_rate:.2f}%")
    logger.info(f"Track validation rate: {track_success_rate:.2f}%")
    elapsed = time.time() - now
    logger.info(f"Pipeline completed in {elapsed:.2f} seconds.")

    artist_file_path = "data/validated/artists.json"
    album_file_path = "data/validated/albums.json"
    track_file_path = "data/validated/tracks.json"

    raw_artist_file_path = "data/raw/artists.json"
    raw_album_file_path = "data/raw/albums.json"
    raw_track_file_path = "data/raw/tracks.json"


    save_json(artist_ls, artist_file_path)
    save_json(album_ls, album_file_path)
    save_json(raw_artist_ls, raw_artist_file_path)
    save_json(raw_album_ls, raw_album_file_path)
    save_json(track_ls, track_file_path)
    save_json(raw_track_ls, raw_track_file_path)
    
    logger.info("Uploading validated artists")
    export_to_s3(artist_file_path, f'validated/artists/{run_date}.json')
    logger.info("Uploading validated albums")
    export_to_s3(album_file_path, f'validated/albums/{run_date}.json')

    logger.info("Uploading raw artists")
    export_to_s3(raw_artist_file_path, f'raw/artists/{run_date}.json')
    logger.info("Uploading raw albums")
    export_to_s3(raw_album_file_path, f'raw/albums/{run_date}.json')

    logger.info("Uploading validated tracks")
    export_to_s3(track_file_path, f'validated/tracks/{run_date}.json')    
    logger.info("Uploading raw tracks")
    export_to_s3(raw_track_file_path, f'raw/tracks/{run_date}.json')
if __name__=="__main__":
    print("Pipeline Starting")
    main()