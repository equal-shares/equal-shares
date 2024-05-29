@echo off

REM Build and run the tests

docker compose -f test.docker-compose.yaml up --build

pause
