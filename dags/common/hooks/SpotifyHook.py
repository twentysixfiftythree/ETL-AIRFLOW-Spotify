import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime, timedelta
from airflow.hooks.base import BaseHook
import sys
import os
from ..config.spotify_config import SPOTIFY_CONFIG


class Track:
    def __init__(self, name, artist, album, url, played_at):
        self.name = name
        self.artist = artist
        self.album = album
        self.played_at = played_at
        self.url = url

    def __repr__(self):
        return f"Track(name='{self.name}', artist='{self.artist}', album='{self.album}', played_at='{self.played_at}')"


class SpotifyHook(BaseHook):
    def __init__(self):
        self.CLIENT_ID = SPOTIFY_CONFIG['CLIENT_ID']
        self.CLIENT_SECRET = SPOTIFY_CONFIG['CLIENT_SECRET']
        self.REDIRECT_URI = SPOTIFY_CONFIG['REDIRECT_URI']
        self.SCOPE = SPOTIFY_CONFIG['SCOPE']
        self.refresh_token = SPOTIFY_CONFIG['REFRESH_TOKEN']
        self.access_token = ''
        self.token_expiration = None

    def refresh_access_token(self):
        """
        Refresh the Spotify access token using the stored refresh token.
        """
        sp_oauth = SpotifyOAuth(client_id=self.CLIENT_ID,
                                 client_secret=self.CLIENT_SECRET,
                                 redirect_uri=self.REDIRECT_URI,
                                 scope=self.SCOPE)

        # Using the refresh token to get a new access token
        token_info = sp_oauth.refresh_access_token(self.refresh_token)
        self.access_token = token_info['access_token']
        self.token_expiration = datetime.utcnow() + timedelta(seconds=token_info['expires_in'])  # Store the expiration time
        
        return self.access_token

    def store_access_token(self, access_token):
        """
        Store the access token for future use.
        This is a placeholder method and should be implemented
        to store the token securely in a database or environment.
        """
        # Store the token securely (in Airflow Variables, Database, or Secret Manager)
        print(f"Access token stored: {access_token}")

    def get_access_token(self):
        """
        Get a valid access token. Refresh it if expired.
        """

        # If no token or it has expired, refresh the token
        if not self.access_token or self.token_expired():
            print("Access token expired, refreshing...")
            self.refresh_access_token()

        return self.access_token

    def token_expired(self):
        """
        Check if the access token is expired by comparing with the stored expiration time.
        """
        if self.token_expiration:
            return datetime.utcnow() > self.token_expiration
        return True  # If there's no expiration time, treat token as expired

    def get_recently_played(self):
        """
        Retrieve recently played tracks from Spotify.
        """
        # Get a valid access token
        access_token = self.get_access_token()

        # Create a Spotify object using the valid access token
        sp = spotipy.Spotify(auth=access_token)

        # Fetch the recently played tracks
        results = sp.current_user_recently_played(limit=50)  # Adjust the limit as needed
        
        recently_played_tracks = []
        today = datetime.today().date()

        # Loop through the results and extract the track information
        for item in results['items']:
            track = item['track']
            track_obj = Track(
                name=track['name'],
                artist=track['artists'][0]['name'],  # Get the first artist name
                album=track['album']['name'],
                url=track['external_urls']['spotify'],
                played_at=item['played_at']  # Time when the track was played
            )
            # Filter by today's date
            if track_obj.played_at.startswith(str(today)):
                recently_played_tracks.append(track_obj)
        
        return recently_played_tracks
