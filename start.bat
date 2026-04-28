@echo off
title Kernel-Tools - Installation and Launch
color 0A

REM # Copyright (c) Kernel-Tool
REM # See the file 'LICENSE' for copying permission

echo ========================================
echo    Kernel-Tools - Auto Setup
echo ========================================
echo.

REM Check if Python 3.11 is already installed
python --version 2>nul | findstr /R "3\.11" >nul
if %errorlevel% equ 0 (
    echo [OK] Python 3.11 is already installed
    echo [INFO] Updating pip...
    python -m pip install --upgrade pip
    echo.
    goto install_requirements
)

echo [INFO] Python 3.11 not detected
echo [INFO] Downloading Python 3.11.9...

set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
set PYTHON_INSTALLER=python-3.11.9-installer.exe

echo Downloading, please wait...
powershell -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo [ERROR] Failed to download Python
    pause
    exit /b 1
)

echo [INFO] Installing Python 3.11.9...
echo Please wait, this may take a few minutes...

"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 AssociateFiles=1

echo [INFO] Waiting for installation to complete...
timeout /t 10 /nobreak >nul

echo [INFO] Cleaning up installer...
del "%PYTHON_INSTALLER%"

echo [OK] Python 3.11.9 installed successfully
echo.

REM ✅ FIX PATH - Recharger les variables d'environnement sans relancer le CMD
echo [INFO] Refreshing PATH...
for /f "tokens=2*" %%A in ('reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYS_PATH=%%B"
for /f "tokens=2*" %%A in ('reg query "HKCU\Environment" /v Path 2^>nul') do set "USR_PATH=%%B"
set "PATH=%SYS_PATH%;%USR_PATH%"

echo [INFO] Updating pip...
python -m pip install --upgrade pip
echo.

:install_requirements
echo ========================================
echo    Installing Dependencies
echo ========================================
echo.

if not exist "requirements.txt" (
    echo [ERROR] requirements.txt file not found
    pause
    exit /b 1
)

echo [INFO] Installing packages from requirements.txt...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo [OK] Dependencies installed successfully
echo.

:launch_tool
echo ========================================
echo    Launching Kernel-Tools
echo ========================================
echo.

if not exist "kernel.py" (
    echo [ERROR] File 'kernel.py' not found
    pause
    exit /b 1
)

echo [INFO] Launching kernel.py...
echo.
python "kernel.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] The program exited with an error
    pause
    exit /b 1
)

echo.
echo [INFO] Program finished
pause
