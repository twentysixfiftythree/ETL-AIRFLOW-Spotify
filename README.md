# Spotify ETL Pipeline

An automated data pipeline that extracts your Spotify listening history, transforms it, and loads it into a MySQL database using Apache Airflow and Docker.

## Overview

This project creates an ETL (Extract, Transform, Load) pipeline that:
- Extracts recently played tracks from Spotify's API
- Transforms the JSON data into a structured format
- Loads the data into a MySQL database
- Runs automatically on a schedule using Airflow

## Tech Stack

- **Apache Airflow**: Workflow orchestration
- **Docker**: Containerization
- **MySQL**: Data storage
- **Python**: Data processing
- **Spotify API**: Data source

## Prerequisites

- Docker and Docker Compose
- Spotify Developer Account
- AWS RDS MySQL instance (or local MySQL server)

## Project Structure

spotify-etl/
├── docker-compose.yaml # Docker configuration
├── Dockerfile # Custom Airflow image
├── dags/
│ ├── spotify_etl_dag.py # Main DAG file
│ ├── common/
│ │ ├── hooks/ # Custom hooks
│ │ └── config/ # Configuration files
│ └── etl/ # ETL logic
└── requirements.txt # Python dependencies



## Setup Instructions

### 1. Spotify API Configuration

1. Create a Spotify Developer account:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application
   - Note your Client ID and Client Secret
   - Add `http://localhost:8888/callback` to your Redirect URIs

2. Configure Spotify credentials:
   ```bash
   cp dags/common/config/spotify_config.template.py dags/common/config/spotify_config.py
   ```
   Update with your credentials:
   ```python
   SPOTIFY_CONFIG = {
       'CLIENT_ID': 'your_client_id',
       'CLIENT_SECRET': 'your_client_secret',
       'REDIRECT_URI': 'http://localhost:8888/callback',
       'SCOPE': 'user-read-recently-played'
   }
   ```

### 2. Docker Setup

1. Build and start the containers found here :
2. cd to the correct path where your files are according to this guide
3. Run docker-compose up airflow-init
   ```bash
   docker-compose up
   ```

3. The following services will be available:
   - Airflow Webserver: http://localhost:8080
   - Airflow Scheduler
   - MySQL Database

### 3. Airflow Configuration

1. Access Airflow UI:
   - URL: http://localhost:8080
   - Default credentials:
     - Username: airflow
     - Password: airflow

2. Configure MySQL Connection:
   - Go to Admin → Connections
   - Add new connection:
     ```
     Connection Id: mysql_connection
     Connection Type: MySQL
     Host: your-rds-endpoint.region.rds.amazonaws.com
     Schema: spotify_db
     Login: your_username
     Password: your_password
     Port: 3306
     ```

### 4. Running the Pipeline

1. The DAG will automatically run on schedule
2. For manual execution:
   - Open Airflow UI
   - Navigate to DAGs
   - Find 'spotify_etl'
   - Click "Trigger DAG"

## Data Model


## Pipeline Details

### Extract
- Connects to Spotify API
- Retrieves recently played tracks
- Handles API rate limiting and authentication

### Transform
- Cleans and structures the data
- Extracts relevant fields
- Handles duplicates and null values

### Load
- Creates tables if they don't exist
- Loads transformed data
- Handles data integrity

## Monitoring and Maintenance

- View logs in Airflow UI
- Check task status and history
- Monitor database growth
- Task retries configured for resilience

## Troubleshooting

Common issues and solutions:
1. **Spotify API Connection Issues**
   - Check token validity
   - Verify credentials in config

2. **Database Connection Issues**
   - Verify RDS security group settings
   - Check connection credentials

3. **Docker Issues**
   - Ensure ports aren't in use
   - Check Docker logs:
     ```bash
     docker-compose logs -f
     ```

## Development

To modify the pipeline:
1. Clone the repository
2. Make changes in the `dags` directory
3. Docker will automatically sync changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License - feel free to use this project as you wish.
