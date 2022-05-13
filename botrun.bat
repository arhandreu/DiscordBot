@echo off

call %~dp0venv\Scripts\activate

cd %~dp0bot

set TOKEN=

python botrun.py

pause
