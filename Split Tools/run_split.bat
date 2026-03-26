@echo off
setlocal

set "SCRIPT_DIR=%~dp0"
set "PYTHON_BIN="

where py >nul 2>nul
if %errorlevel%==0 (
  set "PYTHON_BIN=py -3"
) else (
  where python >nul 2>nul
  if %errorlevel%==0 (
    set "PYTHON_BIN=python"
  )
)

if "%PYTHON_BIN%"=="" (
  echo [run_split.bat] Python 3 not found.
  pause
  exit /b 2
)

call %PYTHON_BIN% "%SCRIPT_DIR%run_split.py" %*
set "STATUS=%ERRORLEVEL%"
echo.
pause
exit /b %STATUS%
