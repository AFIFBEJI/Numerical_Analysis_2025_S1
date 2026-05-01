@echo off
setlocal
cd /d "%~dp0"
set "LOCAL_IP="
for /f "tokens=* delims=" %%i in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -notlike ''127.*'' -and $_.IPAddress -notlike ''169.254.*'' -and $_.PrefixOrigin -ne ''WellKnown'' } | Select-Object -First 1 -ExpandProperty IPAddress)"') do set "LOCAL_IP=%%i"
if "%LOCAL_IP%"=="" set "LOCAL_IP=(not found)"

echo ===========================================
echo Starting LAN static server on port 3000
echo Open this PC:      http://localhost:3000
echo Open other laptop: http://%LOCAL_IP%:3000
echo Press Ctrl+C to stop.
echo ===========================================
echo.

where python >nul 2>&1
if %errorlevel%==0 (
  start "" "http://localhost:3000"
  python -m http.server 3000 --bind 0.0.0.0
  goto :eof
)

where py >nul 2>&1
if %errorlevel%==0 (
  start "" "http://localhost:3000"
  py -3 -m http.server 3000 --bind 0.0.0.0
  goto :eof
)

echo Python was not found.
echo Install Python 3 and run this file again.
pause
