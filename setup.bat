@echo off
REM    Financial Health Asses  nt Platform - Setup Script for Windows
REM This script sets up the development environment for both backend and frontend

echo =========================================
echo    FinHealth AI - Setup Script (Windows)
echo =========================================
echo.

REM Check if Python is installed
echo Checking prerequisites...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3 is not installed. Please install Python 3.9 or higher.
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed. Please install Node.js 16 or higher.
    exit /b 1
)

echo [OK] Python found
python --version
echo [OK] Node.js found
node --version
echo.

REM Backend Setup
echo =========================================
echo Setting up Backend...
echo =========================================

cd backend

REM Create virtual environment
echo Creating Python virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo [WARNING] Please edit backend\.env and add your configuration
    echo   - OPENAI_API_KEY (optional, will use rule-based fallback^)
    echo   - SECRET_KEY (generate with: openssl rand -hex 32^)
    echo   - ENCRYPTION_KEY (generate with: openssl rand -hex 16^)
) else (
    echo [OK] .env file already exists
)

echo [OK] Backend setup complete
echo.

REM Frontend Setup
echo =========================================
echo Setting up Frontend...
echo =========================================

cd ..\frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

echo [OK] Frontend setup complete
echo.

REM Final Instructions
echo =========================================
echo Setup Complete!
echo =========================================
echo.
echo Next steps:
echo.
echo 1. Configure environment variables:
echo    cd backend
echo    notepad .env
echo.
echo 2. Start the backend server:
echo    cd backend
echo    venv\Scripts\activate
echo    uvicorn main:app --reload
echo    # Server will run on http://localhost:8000
echo.
echo 3. In a new terminal, start the frontend:
echo    cd frontend
echo    npm start
echo    # App will run on http://localhost:3000
echo.
echo 4. Open your browser and navigate to http://localhost:3000
echo.
echo Happy coding! 🚀

cd ..
pause
