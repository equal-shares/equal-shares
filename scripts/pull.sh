set -x #echo on
cd /app/equal-shares

git pull

# Update dependencies
cd /app/equal-shares/backend
poetry install --sync

cd /app/equal-shares/frontend
npm ci

# Build the frontend
export $(xargs < /app/frontend.env)

cd /app/equal-shares/frontend
npm run build

rm -rf /app/static
cp -r /app/equal-shares/frontend/dist /app/static

# Restart the services
sudo systemctl restart nginx
sudo systemctl restart equal_shares
