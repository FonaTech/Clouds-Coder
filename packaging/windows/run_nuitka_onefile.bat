@echo off
setlocal EnableExtensions

for %%I in ("%~dp0..\..") do set "ROOT=%%~fI"
set "EXE=%ROOT%\dist\nuitka\web-session-agent-nuitka-onefile.exe"
if not exist "%EXE%" (
  echo [error] executable not found: %EXE%
  echo [hint] Run packaging\windows\build_nuitka_onefile.bat first.
  exit /b 1
)

set "HOST=0.0.0.0"
set "PORT=8080"
set "EXTRA="

:parse
if "%~1"=="" goto run
if /I "%~1"=="--host" (
  if "%~2"=="" goto badarg
  set "HOST=%~2"
  shift
  shift
  goto parse
)
if /I "%~1"=="--port" (
  if "%~2"=="" goto badarg
  set "PORT=%~2"
  shift
  shift
  goto parse
)
set "EXTRA=%EXTRA% %1"
shift
goto parse

:badarg
echo [error] Missing value for %1
exit /b 2

:run
echo [run] %EXE% --host %HOST% --port %PORT%%EXTRA%
"%EXE%" --host "%HOST%" --port "%PORT%"%EXTRA%
exit /b %ERRORLEVEL%
