@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"

set "EXE=%~dp0tools\wechat_exp.exe"

if not exist "%EXE%" (
  echo 尚未安装 WeChat EXP，先自动安装...
  call "%~dp0一键安装.bat"
  if errorlevel 1 exit /b 1
)

echo 正在启动 WeChat EXP...
start "" "%EXE%"

echo 等待本地服务启动...
timeout /t 5 /nobreak >nul

echo 打开聊天导出页面...
start "" "http://127.0.0.1:5000/export"

echo.
echo 如果这是第一次使用，请先回到首页执行一次“一键备份”。
echo 导出完成后，把 TXT / JSON / JSONL 文件直接拖给 ChatGPT。
echo.
timeout /t 3 /nobreak >nul
exit /b 0
