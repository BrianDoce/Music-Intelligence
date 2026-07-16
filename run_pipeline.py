from utils.logger import get_logger
from ingestion.albums import get_artist_albums
from ingestion.artists import get_artist_info
from validation.album_validation import album_validation
from validation.artist_validation import artist_validation
from api.SpotifyClient import SpotifyClient
from utils.savejson import save_json
from utils.s3uploader import export_to_s3
import pandas as pd
import time

def main():
    now = time.time()
    logger = get_logger("spotify_pipeline")
    artist_ids = pd.read_csv("data/tracked_artists.csv")["artist_id"].tolist()
    
    artist_ls = []
    raw_artist_ls = []

    album_ls = []
    raw_album_ls = []

    valid_artists = 0
    invalid_artists = 0

    valid_albums = 0
    invalid_albums = 0

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
            raw_album_ls.extend(raw_album_info)
            for album in album_records:
                logger.info(f"Processing album {album['album_name']}")
                if album_validation(album):
                    valid_albums += 1
                    album_ls.append(album)
                    logger.info(f"Album {album['album_name']} validated successfully.")     
                else:
                    invalid_albums += 1
                    logger.warning(f"Album {album['album_name']} failed validation.")
            time.sleep(1)
        except Exception as e:
            logger.error(f"Error processing artist ID {artist_id}: {e}")


    logger.info(f"Artists processed: {len(artist_ids)}")
    logger.info(f"Albums processed: {len(album_ls)}")

    logger.info(f"Artists collected: {len(artist_ls)}")
    logger.info(f"Albums collected: {len(album_ls)}")

    logger.info(f"Artists validated: {valid_artists}, Invalid artists: {invalid_artists}")
    logger.info(f"Albums validated: {valid_albums}, Invalid albums: {invalid_albums}")

    elapsed = time.time() - now
    logger.info(f"Pipeline completed in {elapsed:.2f} seconds.")

    artist_file_path = "data/validated/artists.json"
    album_file_path = "data/validated/albums.json"

    raw_artist_file_path = "data/raw/raw_artists.json"
    raw_album_file_path = "data/raw/raw_albums.json"

    save_json(artist_ls, artist_file_path)
    save_json(album_ls, album_file_path)
    save_json(raw_artist_ls, raw_artist_file_path)
    save_json(raw_album_ls, raw_album_file_path)
    
    export_to_s3(artist_file_path, 'validated/artists.json')
    export_to_s3(album_file_path, 'validated/albums.json')

    export_to_s3(raw_artist_file_path, 'raw/raw_artists.json')
    export_to_s3(raw_album_file_path, 'raw/raw_albums.json')
    
if __name__=="__main__":
    print("Pipeline Starting")
    main()