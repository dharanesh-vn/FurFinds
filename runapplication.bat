@echo off
setlocal

echo Starting FurFinds application...

if not exist ".venv\Scripts\activate.bat" (
    echo Backend virtual environment not found.
    echo Please run setupdev.bat first.
    exit /b 1
)

if not exist "frontend\package.json" (
    echo Frontend project not found at frontend\package.json.
    exit /b 1
)

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH.
    exit /b 1
)

where npm >nul 2>nul
if errorlevel 1 (
    echo npm was not found on PATH.
    exit /b 1
)

for /f "tokens=5" %%p in ('netstat -ano ^| findstr /R /C:":8000 .*LISTENING"') do (
    echo Port 8000 is already in use by PID %%p.
    echo Close that process and run this script again so FurFinds starts correctly.
    exit /b 1
)

echo Launching FastAPI backend on http://127.0.0.1:8000 ...
start "FurFinds Backend" cmd /k "cd /d %~dp0 && call .venv\Scripts\activate.bat && python -m uvicorn --app-dir ""%~dp0"" main:app --reload --host 127.0.0.1 --port 8000"

echo Launching React frontend on http://localhost:5173 ...
start "FurFinds Frontend" cmd /k "cd /d %~dp0frontend && call npm run dev"

echo.
echo FurFinds backend and frontend are starting in separate windows.
