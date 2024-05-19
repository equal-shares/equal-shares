set -x #echo on
cd /app/equal-shares

git pull

# update permissions
chmod 744 /app/**

# restart the services
docker compose -f prod.docker-compose.yaml down
docker compose -f prod.docker-compose.yaml up --detach --build
