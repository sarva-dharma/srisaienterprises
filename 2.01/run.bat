@echo off
title TaskFlow Studio - Full Stack Website
echo ========================================================
echo   Launching TaskFlow Studio Web Application...
echo   Backend: Python Flask + SQLite REST API
echo   Frontend: Modern Responsive Web Application
echo ========================================================
echo.
echo Opening browser at http://127.0.0.1:5000 in 3 seconds...
start "" http://127.0.0.1:5000
python app.py
pause
