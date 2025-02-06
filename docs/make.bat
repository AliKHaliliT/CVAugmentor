@echo off
setlocal

:: Set the directory where the batch file is being run from
set BUILD_DIR=%CD%\_build

:: Create the build directory if it doesn't exist
if not exist "%BUILD_DIR%" mkdir "%BUILD_DIR%"

:: Run Sphinx build command
sphinx-build -b html . "%BUILD_DIR%\html"

:: Move the HTML contents to the current directory
xcopy /e /i /h "%BUILD_DIR%\html\*" "%CD%\" > nul

:: Clean up the build directory
rd /s /q "%BUILD_DIR%"

echo Documentation has been built and moved to the current directory.

endlocal
