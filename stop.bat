@echo off
REM Financial Data Processing System - Windows Shutdown Script
REM This script stops the running server gracefully

setlocal enabledelayedexpansion

REM Configuration
set "PROJECT_DIR=%~dp0"
set "PID_FILE=%PROJECT_DIR%server.pid"

echo [INFO] === Financial Data Processing System Shutdown ===

REM Change to project directory
cd /d "%PROJECT_DIR%"

REM Check if server is running
if exist "%PID_FILE%" (
    set /p PID=<"%PID_FILE%"
    tasklist /FI "PID eq !PID!" 2>NUL | find /I "!PID!" >NUL
    if !errorlevel! equ 0 (
        echo [INFO] Stopping server (PID: !PID!)...
        
        REM Try graceful shutdown first
        taskkill /PID !PID! >NUL 2>&1
        
        REM Wait for graceful shutdown
        for /l %%i in (1,1,10) do (
            tasklist /FI "PID eq !PID!" 2>NUL | find /I "!PID!" >NUL
            if !errorlevel! neq 0 (
                echo [SUCCESS] Server stopped gracefully
                del "%PID_FILE%" >NUL 2>&1
                goto :cleanup
            )
            timeout /t 1 /nobreak >NUL
        )
        
        REM Force kill if still running
        echo [WARNING] Server didn't stop gracefully, force killing...
        taskkill /PID !PID! /F >NUL 2>&1
        timeout /t 1 /nobreak >NUL
        
        tasklist /FI "PID eq !PID!" 2>NUL | find /I "!PID!" >NUL
        if !errorlevel! neq 0 (
            echo [SUCCESS] Server force stopped
            del "%PID_FILE%" >NUL 2>&1
        ) else (
            echo [ERROR] Failed to stop server
            pause
            exit /b 1
        )
    ) else (
        echo [WARNING] PID file exists but process not found, cleaning up...
        del "%PID_FILE%" >NUL 2>&1
    )
) else (
    echo [WARNING] No server is currently running
)

:cleanup
REM Cleanup any remaining uvicorn processes
echo [INFO] Cleaning up any remaining uvicorn processes...
taskkill /IM python.exe /FI "WINDOWTITLE eq uvicorn*" /F >NUL 2>&1
wmic process where "name='python.exe' and commandline like '%%uvicorn%%'" delete >NUL 2>&1

echo [SUCCESS] === Shutdown Complete ===
pause
