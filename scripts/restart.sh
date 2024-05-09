set -x #echo on
cd /app/equal-shares

# Restart the services
sudo systemctl restart gunicorn
sudo systemctl restart nginx
