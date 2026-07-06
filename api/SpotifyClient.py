import os
import requests

class SpotifyClient:
    def __init__(self):
        self.CLIENT_ID = os.environ.get('SPOTIFY_ID')
        self.CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET')
        self.session = requests.Session()

        self.ACCESS_TOKEN = self.get_access_token()

        self.URL_HEADER = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        self.URL_BASE = 'https://api.spotify.com/v1'

    def paginate(self, url):
        results = []
        while url:
            response = self.session.get(url, headers=self.URL_HEADER)
            response.raise_for_status()
            data = response.json()
            results.extend(data.get('items', []))
            url = data.get('next')
        return results

    def get_access_token(self):
        URL='https://accounts.spotify.com/api/token'
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        data={'grant_type': 'client_credentials', 'client_id': self.CLIENT_ID, 'client_secret': self.CLIENT_SECRET}

        
        request = self.session.post(URL, headers=headers, data=data)
        self.ACCESS_TOKEN = request.json()['access_token']
        self.URL_HEADER = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        return self.ACCESS_TOKEN

    def get_artist_info(self, artist_id):
        URL = f'{self.URL_BASE}/artists/{artist_id}'
        response = self.session.get(URL, headers=self.URL_HEADER)
        return response.json()
    
    def get_artist_albums(self, artist_id):
        URL = f'{self.URL_BASE}/artists/{artist_id}/albums?limit=50'
        return self.paginate(URL)

    def get_album(self, album_id):
        URL = f'{self.URL_BASE}/albums/{album_id}'
        response = self.session.get(URL, headers=self.URL_HEADER)
        return response.json()