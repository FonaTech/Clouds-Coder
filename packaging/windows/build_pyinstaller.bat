@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..\..") do set "ROOT=%%~fI"
set "PYTHON_BIN=%PYTHON%"
if "%PYTHON_BIN%"=="" set "PYTHON_BIN=python"

echo [build] PyInstaller on Windows
echo [build] root=%ROOT%

"%PYTHON_BIN%" -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onedir ^
  --name web-session-agent-pyinstaller ^
  --distpath "%ROOT%\dist\pyinstaller" ^
  --workpath "%ROOT%\build\pyinstaller" ^
  --specpath "%ROOT%\build\pyinstaller" ^
  "%ROOT%\Clouds_Coder.py"
if errorlevel 1 (
  echo [error] PyInstaller build failed.
  exit /b 1
)

set "EXE=%ROOT%\dist\pyinstaller\web-session-agent-pyinstaller\web-session-agent-pyinstaller.exe"
if not exist "%EXE%" (
  echo [error] Built executable not found: %EXE%
  exit /b 1
)

"%EXE%" --help >nul
if errorlevel 1 (
  echo [error] Smoke test failed: executable cannot run --help
  exit /b 1
)

echo [ok] PyInstaller build complete.
echo [ok] executable=%EXE%
exit /b 0
