@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..\..") do set "ROOT=%%~fI"
set "PYTHON_BIN=%PYTHON%"
if "%PYTHON_BIN%"=="" set "PYTHON_BIN=python"

echo [build] PyInstaller onefile on Windows
echo [build] root=%ROOT%

"%PYTHON_BIN%" -m PyInstaller ^
  --noconfirm ^
  --clean ^
  --onefile ^
  --name web-session-agent-pyinstaller-onefile ^
  --distpath "%ROOT%\dist\pyinstaller" ^
  --workpath "%ROOT%\build\pyinstaller_onefile" ^
  --specpath "%ROOT%\build\pyinstaller_onefile" ^
  "%ROOT%\Clouds_Coder.py"
if errorlevel 1 (
  echo [error] PyInstaller onefile build failed.
  exit /b 1
)

set "EXE=%ROOT%\dist\pyinstaller\web-session-agent-pyinstaller-onefile.exe"
if not exist "%EXE%" (
  echo [error] Built executable not found: %EXE%
  exit /b 1
)

"%EXE%" --help >nul
if errorlevel 1 (
  echo [error] Smoke test failed: executable cannot run --help
  exit /b 1
)

echo [ok] PyInstaller onefile build complete.
echo [ok] executable=%EXE%
exit /b 0
