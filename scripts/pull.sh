set -x #echo on
cd /app/equal-shares

git pull

# Update dependencies
cd /app/equal-shares/backend
poetry install

cd /app/equal-shares/frontend
npm ci

# Build the frontend
cd /app/equal-shares/frontend
npm run build

# Restart the services
sudo systemctl restart uvicorn
sudo systemctl restart nginx
