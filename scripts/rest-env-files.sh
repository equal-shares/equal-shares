set -x #echo on
cd /app/equal-shares

# reset the env files
cp /app/equal-shares/prod/backend.env /app/backend.env
cp /app/equal-shares/prod/db.env /app/db.env
cp /app/equal-shares/prod/frontend.env /app/frontend.env

chmod 744 /app/backend.env
chmod 744 /app/db.env
chmod 744 /app/frontend.env
