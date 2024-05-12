set -x #echo on
cd /app/equal-shares

cp -f /app/equal-shares/prod/equal_shares.service /etc/systemd/system/equal_shares.service

systemctl daemon-reload
sudo systemctl restart equal_shares