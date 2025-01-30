from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import logging
from etl.extract import extract_spotify_data
from etl.transform import transform_tracks
from etl.load import load_to_staging

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

def extract():
    logging.info("Starting extraction process...")
    raw_tracks = extract_spotify_data()
    
    # Convert Track objects to dictionaries
    serializable_tracks = [
        {
            'name': track.name,
            'artist': track.artist,
            'album': track.album,
            'played_at': track.played_at
        }
        for track in raw_tracks
    ]
    
    logging.info(f"Extracted {len(serializable_tracks)} tracks from Spotify")
    print(f"Sample of first track: {serializable_tracks[0] if serializable_tracks else 'No data'}")
    return serializable_tracks

def transform(**context):
    logging.info("Starting transformation process...")
    task_instance = context['task_instance']
    raw_data = task_instance.xcom_pull(task_ids='extract_task')
    
    transformed_songs = []
    transformed_albums = []
    
    for track in raw_data:
        # Transform song data
        song_data = {
            'id': f"{track['name']}_{track['artist']}",  # Create a composite key
            'name': track['name'],
            'artist': track['artist'],
            'album': track['album'],
            'played_at': track['played_at']
        }
        
        # Transform album data
        album_data = {
            'id': f"{track['album']}_{track['artist']}", # Create a composite key
            'name': track['album'],
            'artist': track['artist'],
            'release_date': datetime.now().date()  # You might want to get this from Spotify API
        }
        
        transformed_songs.append(song_data)
        transformed_albums.append(album_data)
    
    print(f"Sample transformed song: {transformed_songs[0] if transformed_songs else 'No songs'}")
    print(f"Sample transformed album: {transformed_albums[0] if transformed_albums else 'No albums'}")
    
    task_instance.xcom_push(key='songs', value=transformed_songs)
    task_instance.xcom_push(key='albums', value=transformed_albums)

def load(**context):
    logging.info("Starting load process...")
    task_instance = context['task_instance']
    execution_date = context['execution_date']
    
    print(f"Load task started at: {execution_date}")  # Debug print
    
    songs = task_instance.xcom_pull(task_ids='transform_task', key='songs')
    albums = task_instance.xcom_pull(task_ids='transform_task', key='albums')
    
    print(f"Retrieved {len(songs) if songs else 0} songs from XCom")  # Debug print
    print(f"Retrieved {len(albums) if albums else 0} albums from XCom")  # Debug print
    
    load_to_staging(songs, albums)
    
    logging.info("Load process completed successfully")
    return "Load completed successfully"

with DAG('spotify_etl',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract
    )
    
    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform,
        provide_context=True
    )
    
    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load,
        provide_context=True
    )
    
    # Task dependencies
    extract_task >> transform_task >> load_task 