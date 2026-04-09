@echo off
title Kernel-Tools - Setup and Launch
color 0A

echo ========================================
echo    Kernel-Tools - Auto Setup
echo ========================================
echo.

REM Check if Python 3.14 is already installed
python --version 2>nul | findstr /R "3\.14" >nul
if %errorlevel% equ 0 (
    echo [OK] Python 3.14 is already installed
    echo [INFO] Updating pip...
    python -m pip install --upgrade pip
    echo.
    goto install_requirements
)

echo [INFO] Python 3.14 was not detected
echo [INFO] Downloading Python 3.14.4...

REM Download Python 3.14.4 (latest stable version)
set PYTHON_URL=https://www.python.org/ftp/python/3.14.4/python-3.14.4-amd64.exe
set PYTHON_INSTALLER=python-3.14.4-installer.exe

echo Downloading, please wait...
powershell -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo [ERROR] Failed to download Python
    pause
    exit /b 1
)

echo [INFO] Installing Python 3.14.4...
echo Please wait, this may take a few minutes...

REM Install Python with all features and add to PATH
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 AssociateFiles=1

echo [INFO] Waiting for installation to complete...
timeout /t 5 /nobreak >nul

echo [INFO] Cleaning up installer...
del "%PYTHON_INSTALLER%"

echo [OK] Python 3.14.4 installed successfully
echo.

REM Update pip
echo [INFO] Updating pip...
python -m pip install --upgrade pip
echo.

:install_requirements
echo ========================================
echo    Installing Dependencies
echo ========================================
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo [ERROR] File requirements.txt not found
    echo Make sure this batch file is in the same folder as requirements.txt
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

REM Check if the Python file exists
if not exist "kernel.py" (
    echo [ERROR] File 'kernel.py' not found
    echo Make sure this batch file is in the same folder as the Python script
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
