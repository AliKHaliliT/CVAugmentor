@echo off
REM Batch file to build Sphinx documentation

REM Set the paths
set SOURCE_DIR=.
set BUILD_DIR=docs

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install it first.
    exit /b 1
)

REM Run the augmentations_rst_generator.py script
echo Running augmentations_rst_generator.py...
python augmentations_rst_generator.py

REM Check if the script ran successfully
if errorlevel 1 (
    echo augmentations_rst_generator.py failed.
    exit /b 1
)

REM Check if Sphinx is installed
sphinx-build --version >nul 2>&1
if errorlevel 1 (
    echo Sphinx is not installed. Please install it using 'pip install sphinx'.
    exit /b 1
)

REM Run the Sphinx build command
echo Building Sphinx documentation...
sphinx-build -b html %SOURCE_DIR% %BUILD_DIR%

REM Check if the build was successful
if errorlevel 1 (
    echo Sphinx build failed.
    exit /b 1
)

echo Sphinx build completed successfully.
