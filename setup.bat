@echo off
echo =========================================
echo Chemical Equipment Visualizer Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed
    pause
    exit /b 1
)

echo [OK] Python and Node.js are installed
echo.

REM Setup Backend
echo Setting up Backend...
cd backend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate
pip install -r requirements.txt
echo [OK] Backend dependencies installed

REM Run migrations
python manage.py makemigrations
python manage.py migrate
echo [OK] Database migrations completed

call venv\Scripts\deactivate
cd ..
echo.

REM Setup Web Frontend
echo Setting up Web Frontend...
cd web-frontend

REM Install dependencies
call npm install
echo [OK] Web frontend dependencies installed

cd ..
echo.

REM Setup Desktop Frontend
echo Setting up Desktop Frontend...
cd desktop-frontend

REM Create virtual environment
if not exist "venv" (
    python -m venv venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment and install dependencies
call venv\Scripts\activate
pip install -r requirements.txt
echo [OK] Desktop frontend dependencies installed

call venv\Scripts\deactivate
cd ..
echo.

echo =========================================
echo Setup completed successfully!
echo =========================================
echo.
echo To start the application:
echo.
echo 1. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python manage.py runserver
echo.
echo 2. Start Web Frontend (Terminal 2):
echo    cd web-frontend
echo    npm start
echo.
echo 3. Start Desktop App (Terminal 3):
echo    cd desktop-frontend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo Sample data is available in: sample_data\sample_equipment.csv
echo.
pause

