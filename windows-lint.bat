@echo off

REM Build and run the linters

docker compose -f lint.docker-compose.yaml up --build

pause
