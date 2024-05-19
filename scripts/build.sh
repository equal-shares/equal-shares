set -x #echo on
cd /app/equal-shares

source /app/frontend.env

docker compose -f prod.docker-compose.yaml build --build-arg VITE_API_HOST=$VITE_API_HOST
