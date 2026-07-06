def album_validation(album:dict) -> bool:
    """
    Validates the album data retrieved from the Spotify API.

    Args:
        album (dict): The album data to validate.

    Returns:
        bool: True if the album data is valid, False otherwise.
    """
    if not album.get('artist_id'):
        return False
    if not album.get('album_id') :
        return False
    if not album.get('album_name') or len(album.get('album_name')) == 0:
        return False
    if not isinstance(album.get('release_date'), str):
        return False
    if not isinstance(album.get('total_tracks'), int) or album.get('total_tracks') < 0:
        return False
    
    return True