@echo off
echo Starting FreelanceHub Server...
echo.

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start Django server
python manage.py runserver

pause
