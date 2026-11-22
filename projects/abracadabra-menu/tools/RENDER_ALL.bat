@echo off
rem Renders the 4 TV videos (TV1/TV2 x DAY/NIGHT) from menu-data.js into the "output" folder next to this tools folder.
cd /d "%~dp0"
if not exist "..\output" mkdir "..\output"
for %%S in (1 2) do for %%M in (DAY NIGHT) do (
  echo === TV%%S %%M ===
  node render_menu_video.mjs --screen %%S --mode %%M --out "..\output\TV%%S_%%M.MP4"
  if errorlevel 1 (echo FAILED & pause & exit /b 1)
)
echo.
echo Done. Copy the 4 files from the "output" folder to the USB stick.
pause
