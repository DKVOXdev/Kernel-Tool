@echo off
title Kernel-Tools - Installation et Lancement
color 0A

echo ========================================
echo    Kernel-Tools - Auto Setup
echo ========================================
echo.

REM Vérifier si Python 3.14 est déjà installé
python --version 2>nul | findstr /R "3\.14" >nul
if %errorlevel% equ 0 (
    echo [OK] Python 3.14 est deja installe
    echo [INFO] Mise a jour de pip...
    python -m pip install --upgrade pip
    echo.
    goto install_requirements
)

echo [INFO] Python 3.14 n'est pas detecte
echo [INFO] Telechargement de Python 3.14.3...

REM Télécharger Python 3.14.3 (derniere version stable)
set PYTHON_URL=https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe
set PYTHON_INSTALLER=python-3.14.3-installer.exe

echo Telechargement en cours...
powershell -Command "& {Invoke-WebRequest -Uri '%PYTHON_URL%' -OutFile '%PYTHON_INSTALLER%'}"

if not exist "%PYTHON_INSTALLER%" (
    echo [ERREUR] Echec du telechargement de Python
    pause
    exit /b 1
)

echo [INFO] Installation de Python 3.14.3...
echo Veuillez patienter, cela peut prendre quelques minutes...

REM Installer Python avec toutes les fonctionnalites et ajout au PATH
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 AssociateFiles=1

echo [INFO] Attente de la finalisation de l'installation...
timeout /t 5 /nobreak >nul

echo [INFO] Nettoyage de l'installateur...
del "%PYTHON_INSTALLER%"

echo [OK] Python 3.14.3 installe avec succes
echo.

REM Mise a jour de pip
echo [INFO] Mise a jour de pip...
python -m pip install --upgrade pip
echo.

:install_requirements
echo ========================================
echo    Installation des dependances
echo ========================================
echo.

REM Verifier si requirements.txt existe
if not exist "requirements.txt" (
    echo [ERREUR] Le fichier requirements.txt est introuvable
    echo Assurez-vous que ce fichier batch est dans le meme dossier que requirements.txt
    pause
    exit /b 1
)

echo [INFO] Installation des packages depuis requirements.txt...
python -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)

echo [OK] Dependances installees avec succes
echo.

:launch_tool
echo ========================================
echo    Lancement de Kernel-tools 
echo ========================================
echo.

REM Verifier si le fichier Python existe
if not exist "kernel.py" (
    echo [ERREUR] Le fichier 'kernel.py' est introuvable
    echo Assurez-vous que ce fichier batch est dans le meme dossier que le script Python
    pause
    exit /b 1
)

echo [INFO] Lancement de kernel.py...
echo.
python "kernel.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] Le programme s'est termine avec une erreur
    pause
    exit /b 1
)

echo.
echo [INFO] Programme termine
pause