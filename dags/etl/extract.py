from airflow.providers.mysql.hooks.mysql import MySqlHook
from common.hooks.SpotifyHook import SpotifyHook
import logging

def extract_spotify_data():
    """Extract data from Spotify API"""
    try:
        spotify_hook = SpotifyHook()
        recently_played_tracks = spotify_hook.get_recently_played()
        logging.info(f"Retrieved {len(recently_played_tracks)} tracks from Spotify")
        return recently_played_tracks
    except Exception as e:
        logging.error(f"Error extracting data from Spotify: {e}")
        raise 