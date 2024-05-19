set -x #echo on
cd /app/equal-shares

docker compose -f prod.docker-compose.yaml down
docker compose -f prod.docker-compose.yaml up --detach --build
