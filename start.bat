@echo off
REM Financial Data Processing System - Windows Startup Script
REM This script sets up the virtual environment, installs dependencies, and starts the server

setlocal enabledelayedexpansion

REM Configuration
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%venv"
set "REQUIREMENTS_FILE=%PROJECT_DIR%requirements.txt"
set "MAIN_MODULE=src.api.main:app"
set "HOST=0.0.0.0"
set "PORT=8000"
set "PID_FILE=%PROJECT_DIR%server.pid"
set "LOG_FILE=%PROJECT_DIR%logs\server.log"

REM Create logs directory if it doesn't exist
if not exist "%PROJECT_DIR%logs" mkdir "%PROJECT_DIR%logs"

REM Function to check if server is already running
:check_server_running
if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    tasklist /FI "PID eq !PID!" 2>NUL | find /I "!PID!" >NUL
    if !errorlevel! equ 0 (
        echo [WARNING] Server is already running (PID: !PID!). Stopping it first...
        taskkill /PID !PID! /F >NUL 2>&1
        timeout /t 2 /nobreak >NUL
        del "%PID_FILE%" >NUL 2>&1
        echo [SUCCESS] Existing server stopped
    ) else (
        del "%PID_FILE%" >NUL 2>&1
    )
)

REM Check Python installation
python --version >NUL 2>&1
if !errorlevel! neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [INFO] Found Python !PYTHON_VERSION!

REM Create virtual environment
if not exist "%VENV_DIR%" (
    echo [INFO] Creating virtual environment...
    python -m venv "%VENV_DIR%"
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment and install dependencies
echo [INFO] Activating virtual environment...
call "%VENV_DIR%\Scripts\activate.bat"

echo [INFO] Upgrading pip...
python -m pip install --upgrade pip

if exist "%REQUIREMENTS_FILE%" (
    echo [INFO] Installing dependencies from requirements.txt...
    pip install -r "%REQUIREMENTS_FILE%"
    echo [SUCCESS] Dependencies installed successfully
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Start the server
echo [INFO] Starting Financial Data Processing System server...
echo [INFO] Host: %HOST%
echo [INFO] Port: %PORT%
echo [INFO] Log file: %LOG_FILE%

REM Start server in background
start /B uvicorn %MAIN_MODULE% --host %HOST% --port %PORT% --reload --log-level info > "%LOG_FILE%" 2>&1

REM Get the PID of the last started process
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| find /C "python.exe"') do set PROCESS_COUNT=%%i

REM Wait a moment and check if server started
timeout /t 3 /nobreak >NUL

REM Try to find the uvicorn process PID
for /f "tokens=2" %%i in ('wmic process where "name='python.exe' and commandline like '%%uvicorn%%'" get processid /format:csv ^| find "python.exe"') do (
    echo %%i > "%PID_FILE%"
    goto :server_started
)

:server_started
if exist "%PID_FILE%" (
    set /p SERVER_PID=<"%PID_FILE%"
    echo [SUCCESS] Server started successfully!
    echo [INFO] Server PID: !SERVER_PID!
    echo [INFO] API Documentation: http://%HOST%:%PORT%/docs
    echo [INFO] API Root: http://%HOST%:%PORT%/
    echo [INFO] To view logs: type "%LOG_FILE%"
    echo [INFO] To stop server: stop.bat
) else (
    echo [ERROR] Failed to start server. Check logs: %LOG_FILE%
    pause
    exit /b 1
)

echo [SUCCESS] === Startup Complete ===
pause
