@echo off
echo ============================================================
echo Freelancer Service Booking Platform - Quick Start
echo ============================================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Error creating virtual environment!
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate
echo.

echo Step 3: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error installing dependencies!
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo Step 4: Running migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo Error running migrations!
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo Step 5: Creating initial data...
python setup_project.py
if errorlevel 1 (
    echo Error creating initial data!
    pause
    exit /b 1
)
echo.

echo Step 6: Creating media folders...
if not exist "media" mkdir media
if not exist "media\profiles" mkdir media\profiles
if not exist "media\services" mkdir media\services
if not exist "media\categories" mkdir media\categories
echo Media folders created!
echo.

echo ============================================================
echo Setup completed successfully!
echo ============================================================
echo.
echo Default credentials:
echo   Admin: admin / admin123
echo   Customer: customer1 / customer123
echo   Freelancer: freelancer1 / freelancer123
echo.
echo Starting development server...
echo Access the application at: http://127.0.0.1:8000/
echo Admin panel at: http://127.0.0.1:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python manage.py runserver
