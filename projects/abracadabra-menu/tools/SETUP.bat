@echo off
rem One-time setup on Windows. Needs internet. Run by double-click.
cd /d "%~dp0"
where node >nul 2>nul || (echo Install Node.js LTS first from https://nodejs.org and run this again. & pause & exit /b 1)
where ffmpeg >nul 2>nul || (echo ffmpeg is missing. In a terminal run:  winget install Gyan.FFmpeg   then open a NEW window and run this again. & pause & exit /b 1)
call npm install
call npx playwright install chromium
echo.
echo Setup done. Now use RENDER_ALL.bat
pause
