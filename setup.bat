@echo off
chcp 65001 >nul
cd /d "%~dp0"
if not exist ".env.local" copy ".env.example" ".env.local" >nul
echo.
echo 初始化完成。
echo 请打开 .env.local，把 WEFLOW_TOKEN= 后面填上 WeFlow API Token。
echo 然后双击“一键导出微信聊天.bat”。
echo.
notepad ".env.local"
pause
