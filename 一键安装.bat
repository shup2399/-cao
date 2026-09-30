@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

set "TOOLS=%~dp0tools"
set "EXE=%TOOLS%\wechat_exp.exe"
set "URL=https://github.com/sunhanaix/pc_wechat_exp/releases/download/v2.10.20260928/wechat_exp_2.10.20260928.exe"
set "SHA=000BC70437123D68C953D35D0F95DC0C12C2A5757686BD8F0F04717A9663BB6B"

if not exist "%TOOLS%" mkdir "%TOOLS%"

if exist "%EXE%" (
  echo 已存在 WeChat EXP，开始校验...
  goto verify
)

echo.
echo 正在从 WeChat EXP 官方 GitHub Release 下载...
echo %URL%
echo.

powershell -NoProfile -Command "$ProgressPreference='SilentlyContinue'; Invoke-WebRequest -Uri '%URL%' -OutFile '%EXE%'"
if errorlevel 1 (
  echo.
  echo 下载失败。
  pause
  exit /b 1
)

:verify
for /f "tokens=*" %%H in ('powershell -NoProfile -Command "(Get-FileHash -Algorithm SHA256 '%EXE%').Hash"') do set "ACTUAL=%%H"

if /I not "%ACTUAL%"=="%SHA%" (
  echo.
  echo SHA-256 校验失败！
  echo 预期: %SHA%
  echo 实际: %ACTUAL%
  echo 为安全起见已删除下载文件。
  del /q "%EXE%" >nul 2>nul
  pause
  exit /b 2
)

echo.
echo 安装完成并通过 SHA-256 校验：
echo %EXE%
echo.
pause
exit /b 0
