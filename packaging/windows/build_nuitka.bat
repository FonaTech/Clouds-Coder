@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..\..") do set "ROOT=%%~fI"
set "PYTHON_BIN=%PYTHON%"
if "%PYTHON_BIN%"=="" set "PYTHON_BIN=python"

echo [build] Nuitka on Windows
echo [build] root=%ROOT%

"%PYTHON_BIN%" -m nuitka ^
  --standalone ^
  --assume-yes-for-downloads ^
  --remove-output ^
  --output-dir="%ROOT%\dist\nuitka" ^
  --output-filename=web-session-agent-nuitka.exe ^
  "%ROOT%\Clouds_Coder.py"
if errorlevel 1 (
  echo [error] Nuitka build failed.
  exit /b 1
)

set "EXE=%ROOT%\dist\nuitka\Clouds_Coder.dist\web-session-agent-nuitka.exe"
if not exist "%EXE%" (
  echo [error] Built executable not found: %EXE%
  exit /b 1
)

"%EXE%" --help >nul
if errorlevel 1 (
  echo [error] Smoke test failed: executable cannot run --help
  exit /b 1
)

echo [ok] Nuitka build complete.
echo [ok] executable=%EXE%
exit /b 0
