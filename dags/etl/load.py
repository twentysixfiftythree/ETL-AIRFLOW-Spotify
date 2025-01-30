from airflow.providers.mysql.hooks.mysql import MySqlHook
import logging

def create_schemas_if_not_exist(mysql_hook):
    """Create necessary schemas if they don't exist"""
    queries = [
        "CREATE SCHEMA IF NOT EXISTS staging",
        "CREATE SCHEMA IF NOT EXISTS main"
    ]
    connection = mysql_hook.get_conn()
    cursor = connection.cursor()
    for query in queries:
        cursor.execute(query)
    connection.commit()

def create_tables_if_not_exist(cursor):
    """Create necessary tables if they don't exist"""
    tables = {
        'staging.songs': """
            CREATE TABLE IF NOT EXISTS staging.songs (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                album VARCHAR(255),
                played_at DATETIME
            )
        """,
        'staging.albums': """
            CREATE TABLE IF NOT EXISTS staging.albums (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                release_date DATE
            )
        """,
        'main.songs': """
            CREATE TABLE IF NOT EXISTS main.songs (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                album VARCHAR(255),
                played_at DATETIME
            )
        """,
        'main.albums': """
            CREATE TABLE IF NOT EXISTS main.albums (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                artist VARCHAR(255),
                release_date DATE
            )
        """
    }
    
    for query in tables.values():
        cursor.execute(query)

def load_to_staging(songs, albums):
    """Load transformed data into staging tables"""
    try:
        mysql_hook = MySqlHook(mysql_conn_id='mysql_connection')
        create_schemas_if_not_exist(mysql_hook)
        
        connection = mysql_hook.get_conn()
        cursor = connection.cursor()
        
        create_tables_if_not_exist(cursor)
        
        # Insert songs
        for song in songs:
            cursor.execute("""
                INSERT INTO staging.songs (id, name, artist, album, played_at)
                VALUES (%(id)s, %(name)s, %(artist)s, %(album)s, %(played_at)s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), artist = VALUES(artist), 
                album = VALUES(album), played_at = VALUES(played_at)
            """, song)
        
        # Insert albums
        for album in albums:
            cursor.execute("""
                INSERT INTO staging.albums (id, name, artist, release_date)
                VALUES (%(id)s, %(name)s, %(artist)s, %(release_date)s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), artist = VALUES(artist), 
                release_date = VALUES(release_date)
            """, album)
        
        connection.commit()
        logging.info("Data loaded to staging successfully")
        
        # Move data to main
        cursor.execute("INSERT INTO main.songs SELECT * FROM staging.songs ON DUPLICATE KEY UPDATE name=VALUES(name), artist=VALUES(artist), album=VALUES(album), played_at=VALUES(played_at)")
        cursor.execute("INSERT INTO main.albums SELECT * FROM staging.albums ON DUPLICATE KEY UPDATE name=VALUES(name), artist=VALUES(artist), release_date=VALUES(release_date)")
        connection.commit()
        logging.info("Data loaded to main successfully")
        
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        raise 