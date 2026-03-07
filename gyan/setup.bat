@echo off

echo.
echo ============================================
echo GyaanShelf - gyan folder setup
echo ============================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3] Upgrading pip...
python -m pip install --upgrade pip

echo [4] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [5] Setup Complete!
echo.
echo Next steps:
echo 1. Create MySQL database:
echo    - Open MySQL Command Line Client
echo    - Run: source database.sql
echo
echo 2. Update database credentials in app.py:
echo    - MYSQL_HOST = 'localhost'
echo    - MYSQL_USER = 'your_username'
echo    - MYSQL_PASSWORD = 'your_password'
echo.
echo 3. Run the application:
echo    - python app.py
echo.
echo 4. Open browser and go to: http://localhost:5000
echo.
pause