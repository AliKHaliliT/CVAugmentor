@echo off
REM Batch file to build Sphinx documentation

REM Set the paths
set SOURCE_DIR=.
set BUILD_DIR=_build

REM Check if Sphinx is installed
sphinx-build --version >nul 2>&1
if errorlevel 1 (
    echo Sphinx is not installed. Please install it using 'pip install sphinx'.
    pause
    exit /b 1
)

REM Run the Sphinx build command
echo Building Sphinx documentation...
sphinx-build -b html %SOURCE_DIR% %BUILD_DIR%

REM Check if the build was successful
if errorlevel 1 (
    echo Sphinx build failed.
    pause
    exit /b 1
)

echo Sphinx build completed successfully.
pause