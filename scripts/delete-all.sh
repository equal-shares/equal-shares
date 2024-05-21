set -x #echo on
cd /app/equal-shares

# Delete all containers and volumes

docker compose -f prod.docker-compose.yaml stop
docker compose -f prod.docker-compose.yaml rm -v -f
