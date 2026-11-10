@echo off
setlocal enabledelayedexpansion

:: 1. Anchor working directory to script location
cd /d "%~dp0"

title SINGULARITY - Black Hole Simulation

echo =====================================================================
echo    SINGULARITY - Arabic Gravitational Art Engine
echo =====================================================================
echo.

:: 2. Check for Python installation
where python >nul 2>nul
if %ERRORLEVEL% neq 0 goto :NO_PYTHON

:: 3. Setup Virtual Environment if missing
if not exist ".venv\Scripts\python.exe" goto :CREATE_VENV
goto :CHECK_DEPS

:CREATE_VENV
echo [*] Virtual environment not found. Creating .venv ...
python -m venv .venv
if %ERRORLEVEL% neq 0 goto :VENV_FAILED
echo [*] Virtual environment created successfully.
goto :INSTALL_DEPS

:CHECK_DEPS
:: Check if key package is installed
.venv\Scripts\python.exe -c "import pygame, numpy" >nul 2>nul
if %ERRORLEVEL% equ 0 goto :LAUNCH

:INSTALL_DEPS
echo [*] Installing required dependencies from requirements.txt ...
echo [*] This only happens once or when dependencies are updated.
.venv\Scripts\python.exe -m pip install --upgrade pip --quiet
.venv\Scripts\python.exe -m pip install -r requirements.txt
if %ERRORLEVEL% neq 0 goto :INSTALL_FAILED
echo [*] All dependencies are ready.
echo.

:LAUNCH
echo =====================================================================
echo Launching SINGULARITY...
echo Controls: [C] Cinematic Tour - [H] HUD - [Space] Pause - [Esc] Exit
echo =====================================================================
echo.
.venv\Scripts\python.exe main.py %*
if %ERRORLEVEL% neq 0 goto :RUN_ERROR
goto :END

:NO_PYTHON
echo.
echo [ERROR] Python was not found on your system!
echo.
echo Please install Python 3.11 or higher from https://www.python.org/
echo IMPORTANT: During installation, make sure to check the option:
echo    Add Python to PATH
echo.
pause
exit /b 1

:VENV_FAILED
echo.
echo [ERROR] Failed to create virtual environment .venv.
echo Please verify that Python is installed properly.
echo.
pause
exit /b 1

:INSTALL_FAILED
echo.
echo [ERROR] Failed to install dependencies from requirements.txt.
echo Please check your internet connection and try again.
echo.
pause
exit /b 1

:RUN_ERROR
echo.
echo [ERROR] The application exited with an error code: %ERRORLEVEL%
echo.
pause
exit /b %ERRORLEVEL%

:END
endlocal

