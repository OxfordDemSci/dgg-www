FROM postgis/postgis:15-3.4

RUN apt-get update && apt-get install -y dos2unix

COPY ./init-scripts/ /docker-entrypoint-initdb.d/
#COPY ./postgresql.conf /var/lib/postgresql/data/postgresql.conf

RUN dos2unix /docker-entrypoint-initdb.d/00-remove-crlf.sh
RUN dos2unix /docker-entrypoint-initdb.d/init-db.sh
# RUN dos2unix /var/lib/postgresql/data/postgresql.conf
# CMD ["postgres", "-c", "config_file=/var/lib/postgresql/data/postgresql.conf"]
    