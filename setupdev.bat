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

if exist "requirements.txt" (
    pip install -r requirements.txt
    if errorlevel 1 goto :error
) else (
    pip install fastapi sqlalchemy alembic uvicorn pydantic pytest
    if errorlevel 1 goto :error
)

echo [3/4] Running Alembic migrations...
python -m alembic upgrade head
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
