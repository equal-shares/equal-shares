set -x #echo on
cd /app/equal-shares

cp -f /app/equal-shares/prod/nginx/equal_shares /etc/nginx/sites-available/default
cp -f /app/equal-shares/prod/nginx/equal_shares /etc/nginx/sites-enabled/default

systemctl daemon-reload
sudo systemctl restart nginx
