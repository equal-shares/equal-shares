set -x #echo on
cd /app/equal-shares

docker compose down -f prod.docker-compose.yml
docker compose up -d -f prod.docker-compose.yml
