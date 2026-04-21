@echo off
setlocal

echo [1/4] Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 goto :error
) else (
    echo .venv already exists. Skipping creation.
)

echo [2/4] Installing backend dependencies...
call ".venv\Scripts\activate.bat"
if errorlevel 1 goto :error

python -m pip install --upgrade pip
if errorlevel 1 goto :error

if exist "backend\requirements.txt" (
    pip install -r backend\requirements.txt
    if errorlevel 1 goto :error
) else (
    pip install fastapi sqlalchemy alembic uvicorn pydantic pytest httpx python-dateutil urllib3 chromadb bcrypt pyjwt
    if errorlevel 1 goto :error
)

echo [3/4] Running Alembic migrations...
pushd backend
python -m alembic upgrade head
set "ALEMBIC_EXIT=%errorlevel%"
popd
if not "%ALEMBIC_EXIT%"=="0" goto :error
if errorlevel 1 goto :error

echo [4/4] Installing frontend dependencies...
if exist "frontend\package.json" (
    pushd frontend
    call npm install
    if errorlevel 1 (
        popd
        goto :error
    )
    popd
) else (
    echo frontend\package.json not found. Skipping npm install.
)

echo.
echo Development setup completed successfully.
echo Activate backend env with: call .venv\Scripts\activate.bat
goto :eof

:error
echo.
echo Setup failed. Please review the error output above.
exit /b 1
