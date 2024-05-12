set -x #echo on
cd /app/equal-shares

cp -f /app/equal-shares/prod/nginx/equal_shares /etc/nginx/sites-available/equal_shares
cp -f /app/equal-shares/prod/nginx/equal_shares /etc/nginx/sites-enabled/equal_shares

sudo systemctl reload nginx
