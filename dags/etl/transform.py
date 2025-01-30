import logging
from datetime import datetime

def transform_tracks(raw_tracks):
    """Transform raw track data into songs and albums format"""
    try:
        transformed_songs = []
        transformed_albums = []
        
        # Debug print to see the structure
        print(f"Raw track example: {raw_tracks[0] if raw_tracks else 'No tracks'}")
        
        for track in raw_tracks:
            # Debug print to see track attributes
            print(f"Track attributes: {dir(track)}")
            
            # Transform song data
            song_data = {
                'id': track.track_id,  # or track.spotify_id depending on your SpotifyHook implementation
                'name': track.track_name,  # or track.name
                'artist': track.artist_name,  # or track.artist
                'album': track.album_name,  # or track.album
                'played_at': track.played_at
            }
            
            # Transform album data
            album_data = {
                'id': track.album_id,
                'name': track.album_name,
                'artist': track.artist_name,
                'release_date': track.album_release_date
            }
            
            print(f"Transformed song: {song_data}")  # Debug print
            print(f"Transformed album: {album_data}")  # Debug print
            
            transformed_songs.append(song_data)
            transformed_albums.append(album_data)
        
        logging.info(f"Transformed {len(transformed_songs)} songs and {len(transformed_albums)} albums")
        return transformed_songs, transformed_albums
    
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        print(f"Error details: {str(e)}")  # Debug print
        raise 