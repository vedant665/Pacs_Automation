@echo off
echo ============================================================
echo   PACS Test Automation Portal - Server Setup
echo ============================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.8+
    pause
    exit /b 1
)

echo Installing Python dependencies...
pip install flask flask-cors
echo.

echo Initializing database...
cd server
python -c "import database; database.init_db(); print('Database ready!')"
cd ..
echo.

echo ============================================================
echo   Setup complete!
echo ============================================================
echo.
echo   Default login: admin / admin123
echo.
echo   To start the server:
echo     cd web_page\server
echo     python app.py
echo.
echo   Server will run at: http://localhost:5000
echo.
pause