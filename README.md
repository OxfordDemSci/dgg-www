# dgg-www
<strong>Digital Gender Gaps Web Application</strong>

The Digital Gender Gaps Web Application provides an interactive map to explore national indicators of gender equality in access to the internet and mobile phones and their trends through time. The web application provides intuitive visualisations of spatial data, bulk data downloads, and an API to automate on-the-fly data requests for data scientists and web developers.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version. This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details (see LICENSE file or https://www.gnu.org/licenses/).

### Components

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

## Suggested Citation

If possible, please cite a specific [release version](<https://github.com/OxfordDemSci/dgg-www/releases>) 
using the suggested citation in the release documentation which should include a version number and digital object 
identifier (DOI).

Otherwise, please use the following generic citation:   
>Leasure DR, Yan J, Bondarenko M, Kerr D, Kashyap R. 2023. Digital Gender Gaps Web Application. GitHub. 
https://github.com/OxfordDemSci/dgg-www

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public 
License as published by the Free Software Foundation, either version 3 of the License, or any later version. This 
program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty 
of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details (see 
LICENSE file or <https://www.gnu.org/licenses/>).

