@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 wechat_export.py
) else (
  python wechat_export.py
)
echo.
pause
