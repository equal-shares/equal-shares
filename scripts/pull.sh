set -x #echo on
cd /app/equal-shares

git pull

# update permissions
chmod 744 /app/**

# restart and update the services
VITE_WITHOUT_AUTH_MODE=false

source /app/frontend.env

docker compose -f prod.docker-compose.yaml stop
docker compose -f prod.docker-compose.yaml build \
    --build-arg VITE_API_HOST=$VITE_API_HOST \
    --build-arg VITE_WITHOUT_AUTH_MODE=$VITE_WITHOUT_AUTH_MODE
docker compose -f prod.docker-compose.yaml up --detach

docker compose -f prod.docker-compose.yaml cp ./prod/db/pg_hba.conf db:/var/lib/postgresql/data/pg_hba.conf
docker compose -f prod.docker-compose.yaml restart db

# restart the nginx server
systemctl restart nginx
