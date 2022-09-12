# dgg-www
Digital Gender Gaps website

## Components

1. Leaflet front-end with interactive map.
2. Flask API to query data
3. PostgreSQL database

## Docker Deployment
To launch the app using the Docker deployment, you must first install Docker and Docker-Compose. 
The easiest way to do this may be [Docker Desktop](https://docs.docker.com/desktop/). 
Alternatively, you can install [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/) individually. 

The Docker deployment for this application uses three containers that are defined in `./docker-compose.yml`:  
1. **dgg_web:** An nginx web server (see `./www/`)
2. **dgg_api:** A Flask API running behind a gunicorn WSGI server (see `./api/`)
3. **dgg_db:** A PostgreSQL database (see `./sql/`)

To build and launch the Docker containers from the command line: 
```angular2html
cd .../dgg-www
docker-compose up -d --build
```

You can check the status of active docker containers using:
```angular2html
docker ps
docker stats
```

While the containers are running, you can view the app from your web browser: 
- Navigate to [http://127.0.0.1](http://127.0.0.1) to view the front-end with an interactive web map
- Navigate to [http://127.0.0.1/api/v1](http://127.0.0.1/api/v1) for API documentation


To stop the containers, use:
```angular2html
docker-compose down
```



