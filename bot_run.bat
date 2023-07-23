@echo off

call %~dp0\venv\Scripts\activate

cd

set TOKEN=<ваш токен> 

python bot_telegram.py

pause