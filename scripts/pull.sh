set -x #echo on
cd /app/equal-shares

git pull

# restart the services
docker compose down -f prod.docker-compose.yml
docker compose up -d -f prod.docker-compose.yml
