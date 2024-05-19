set -x #echo on
cd /app/equal-shares

git pull

# restart the services
docker compose -f prod.docker-compose.yml down
docker compose -f prod.docker-compose.yml up --detach --build
