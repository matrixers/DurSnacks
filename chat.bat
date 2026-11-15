@echo off
cd /d "%~dp0"
set PYTHONIOENCODING=utf-8
"%~dp0..\DurSnacks\HugCards\.venv\Scripts\python.exe" -m Backend.chat
pause
