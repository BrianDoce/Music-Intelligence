def artist_validation(artist: dict) -> bool:
    """
    Validates the artist data retrieved from the Spotify API.

    Args:
        artist (dict): The artist data to validate.

    Returns:
        bool: True if the artist data is valid, False otherwise.
    """
    if not artist.get('artist_id') or not artist.get('artist_name'):
        return False
    
    followers = artist.get('followers')
    if followers is None or followers < 0:
        return False
    
    return True