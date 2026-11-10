@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
title SINGULARITY - Build Windows Executable

echo =====================================================================
echo    SINGULARITY - Windows Standalone Executable Builder
echo =====================================================================
echo.

:: Detect Python
if exist ".venv\Scripts\python.exe" (
    set "PYTHON_EXEC=.venv\Scripts\python.exe"
) else (
    set "PYTHON_EXEC=python"
)

where %PYTHON_EXEC% >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python was not found. Please run run.bat first to setup environment.
    pause
    exit /b 1
)

:: Ensure PyInstaller is installed
echo [*] Checking PyInstaller...
"%PYTHON_EXEC%" -m pip show pyinstaller >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [*] Installing PyInstaller into virtual environment...
    "%PYTHON_EXEC%" -m pip install pyinstaller
)

echo [*] Building SINGULARITY standalone executable...
echo [*] Bundling Python runtime, Pygame, NumPy, and Arabic fonts...
echo.

"%PYTHON_EXEC%" -m PyInstaller ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --name "SINGULARITY" ^
    --paths "src" ^
    --collect-all "singularity" ^
    --add-data "assets;assets" ^
    --add-data "config.json;." ^
    --hidden-import "arabic_reshaper" ^
    --hidden-import "bidi" ^
    --hidden-import "bidi.algorithm" ^
    --hidden-import "pygame" ^
    --hidden-import "pygame_ce" ^
    --hidden-import "numpy" ^
    --hidden-import "PIL" ^
    main.py

if %ERRORLEVEL% neq 0 goto :BUILD_FAILED

:: Copy screenshots folder and config to dist
if not exist "dist\SINGULARITY\screenshots" mkdir "dist\SINGULARITY\screenshots"
if exist "config.json" copy /y "config.json" "dist\SINGULARITY\config.json" >nul

:: Create one-click helper scripts in dist
echo @echo off > "dist\Run_App.bat"
echo cd /d "%%~dp0SINGULARITY" >> "dist\Run_App.bat"
echo start "" "SINGULARITY.exe" >> "dist\Run_App.bat"

echo @echo off > "dist\SINGULARITY\Run.bat"
echo cd /d "%%~dp0" >> "dist\SINGULARITY\Run.bat"
echo start "" "SINGULARITY.exe" >> "dist\SINGULARITY\Run.bat"

:: Clean temporary build artifacts
if exist "build" rmdir /s /q "build"
if exist "SINGULARITY.spec" del /q "SINGULARITY.spec"

echo.
echo =====================================================================
echo [SUCCESS] Build completed successfully!
echo Executable is located at: dist\SINGULARITY\SINGULARITY.exe
echo Anyone can now run SINGULARITY without installing Python!
echo =====================================================================
echo.
pause
goto :END

:BUILD_FAILED
echo.
echo [ERROR] PyInstaller build failed with error code: %ERRORLEVEL%
pause
exit /b %ERRORLEVEL%

:END
endlocal

