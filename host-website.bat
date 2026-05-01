@echo off
setlocal
cd /d "%~dp0"

echo Starting local static server for this folder...
echo.
echo Local URL:   http://localhost:3000
echo Press Ctrl+C to stop the server.
echo.

where python >nul 2>&1
if %errorlevel%==0 (
  start "" "http://localhost:3000"
  python -m http.server 3000
  goto :eof
)

where py >nul 2>&1
if %errorlevel%==0 (
  start "" "http://localhost:3000"
  py -3 -m http.server 3000
  goto :eof
)

echo Python was not found on this system.
echo Install Python, then run this file again.
pause
@echo off
setlocal
cd /d "%~dp0"

echo ===========================================
echo Starting local website server...
echo Press Ctrl+C to stop it.
echo ===========================================
echo.

npx serve .

echo.
echo Server stopped.
pause
