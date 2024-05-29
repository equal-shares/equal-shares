@echo off

REM Build and run the services

docker compose -f dev.docker-compose.yaml up --build

pause
