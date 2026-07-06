from utils.logger import get_logger
from ingestion.albums import get_artist_albums
from ingestion.artists import get_artist_info
from validation.album_validation import album_validation
from validation.artist_validation import artist_validation
from api.SpotifyClient import SpotifyClient
import pandas as pd
import time

def main():
    now = time.time()
    logger = get_logger("spotify_pipeline")
    artist_ids = pd.read_csv("data/artist_ids.csv")["artist_id"].tolist()
    
    artist_ls = []
    raw_artist_ls = []

    album_ls = []
    raw_album_ls = []

    valid_artists = 0
    invalid_artists = 0

    valid_albums = 0
    invalid_albums = 0

    client = SpotifyClient()
    albums = []

    for artist_id in artist_ids:
        try:
            artist, raw_artist_info = get_artist_info(client, artist_id)
            if artist_validation(artist):
                valid_artists += 1
                artist_ls.append(artist)
                raw_artist_ls.append(raw_artist_info)
                logger.info(f"Artist {artist['artist_name']} validated successfully.")
            else:
                invalid_artists += 1
                logger.warning(f"Artist {artist['artist_name']} failed validation.")
            
            albums, raw_album_info = get_artist_albums(client, artist_id)
            for album, raw_album in zip(albums, raw_album_info):
                if album_validation(album):
                    valid_albums += 1
                    album_ls.append(album)
                    raw_album_ls.append(raw_album)
                    logger.info(f"Album {album['album_name']} validated successfully.")     
                else:
                    invalid_albums += 1
                    logger.warning(f"Album {album['album_name']} failed validation.")
        except Exception as e:
            logger.error(f"Error processing artist ID {artist_id}: {e}")


    logger.info(f"Artists processed: {len(artist_ids)}")
    logger.info(f"Albums processed: {len(albums)}")

    logger.info(f"Artists collected: {len(artist_ls)}")
    logger.info(f"Albums collected: {len(album_ls)}")

    logger.info(f"Artists validated: {valid_artists}, Invalid artists: {invalid_artists}")
    logger.info(f"Albums validated: {valid_albums}, Invalid albums: {invalid_albums}")

    elapsed = time.time() - now
    logger.info(f"Pipeline completed in {elapsed:.2f} seconds.")

if __name__=="__main__":
    main()