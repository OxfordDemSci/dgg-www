#!/bin/bash

# Function to check if the PostgreSQL database is ready
database_ready() {
    PGPASSWORD="$POSTGRES_PASSWORD" psql -h dgg_postgres -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "SELECT 1" >/dev/null 2>&1
}

# Wait for the PostgreSQL database to become available
while ! database_ready; do
    echo "Waiting for the database to become available..."
    sleep 2
done

# Run insert_data.py 
#python3 ./scripts/insert_data.py
alembic upgrade head

# Start the Flask app
gunicorn --config gunicorn.config.py --preload wsgi:app

