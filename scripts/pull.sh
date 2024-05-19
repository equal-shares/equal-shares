set -x #echo on
cd /app/equal-shares

git pull

# update permissions
chmod 744 /app/**

# restart and update the services
source /app/frontend.env
export $VITE_API_HOST

docker compose -f prod.docker-compose.yaml stop
docker compose -f prod.docker-compose.yaml build --build-arg VITE_API_HOST=$VITE_API_HOST
docker compose -f prod.docker-compose.yaml up --detach
