set -x #echo on
cd /app/equal-shares

docker compose -f prod.docker-compose.yaml exec backend python -m src check-database
