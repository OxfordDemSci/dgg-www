#!/bin/sh
#sed -i 's/\r$//' /docker-entrypoint-initdb.d/init-db.sh
echo "Removing CRLF from all files in /docker-entrypoint-initdb.d"