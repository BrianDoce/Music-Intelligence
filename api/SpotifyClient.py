import os
import requests
import time

class SpotifyClient:
    def __init__(self):
        self.CLIENT_ID = os.environ.get('SPOTIFY_ID')
        self.CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET')
        self.session = requests.Session()

        self.ACCESS_TOKEN = self.get_access_token()

        self.URL_HEADER = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        self.URL_BASE = 'https://api.spotify.com/v1'
        
    def request_with_retry(self, url):
        print(f"GET {url}")
        
        for attempt in range(5):
            response = self.session.get(
                url,
                headers=self.URL_HEADER,
                timeout=15
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 5))
                time.sleep(wait)
                print(
                    f"Rate limited. "
                    f"Attempt {attempt+1}/5. "
                    f"Sleeping {wait} seconds."
                )                
                continue
            if response.status_code != 200:
                print(f"Error: {response.status_code} - {response.text}")
            response.raise_for_status()
            return response.json()

        raise Exception("Spotify request failed after retries")
    def paginate(self, url):
        results = []

        while url:
            data = self.request_with_retry(url)

            results.extend(data.get('items', []))
            url = data.get('next')

            if url:
                time.sleep(1) 
        return results

    def get_access_token(self):
        URL='https://accounts.spotify.com/api/token'
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
        data={'grant_type': 'client_credentials', 'client_id': self.CLIENT_ID, 'client_secret': self.CLIENT_SECRET}

        
        request = self.session.post(URL, headers=headers, data=data, timeout=15)
        print(f"Status: {request.status_code}")
        print(request.json())
        self.ACCESS_TOKEN = request.json()['access_token']
        self.URL_HEADER = {'Authorization': f'Bearer {self.ACCESS_TOKEN}'}
        return self.ACCESS_TOKEN

    def get_artist_info(self, artist_id):
        URL = f'{self.URL_BASE}/artists/{artist_id}'
        
        return self.request_with_retry(URL)
    
    def get_artist_albums(self, artist_id):
        URL = f'{self.URL_BASE}/artists/{artist_id}/albums?include_groups=album&market=US&limit=50'
        return self.paginate(URL)

    def get_album(self, album_id):
        URL = f'{self.URL_BASE}/albums/{album_id}'
        
        return self.request_with_retry(URL)
    
    def get_album_tracks(self, album_id):
        URL = f'{self.URL_BASE}/albums/{album_id}/tracks?market=US&limit=50'

        return self.paginate(URL)