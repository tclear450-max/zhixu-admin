@echo off
cd /d "%~dp0"
docker compose -f compose.delivery.yaml stop
pause
