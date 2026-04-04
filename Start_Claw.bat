@echo off
setlocal enabledelayedexpansion
cd /d "%USERPROFILE%"
chcp 65001 >nul

title OpenClaw V22.20 [Native-Launch] - Rex Master

:: 1. 强力清除僵尸进程
echo [1/4] Purging ghost processes...
taskkill /F /IM node.exe /T 2>nul
taskkill /F /IM openclaw.exe /T 2>nul
timeout /t 1 /nobreak >nul

:: 2. 安全注入变量 (跳过带 # 的注释行)
if exist ".env.openclaw" (
    for /f "usebackq tokens=*" %%a in (".env.openclaw") do (
        set "line=%%a"
        if "!line:~0,1!" neq "#" set "%%a"
    )
    echo [OK] Environment variables injected.
)

:: 3. 驱动重定向
set "OPENAI_API_KEY=%DEEPSEEK_API_KEY%"
set "OPENAI_API_BASE=https://api.deepseek.com/v1"
set "ANTHROPIC_API_KEY=none"

:: 4. 修正后的启动指令 (移除 --host)
echo [STEP 4] 点火网关...
echo ---------------------------------------------------
echo [URL] http://127.0.0.1:18789
echo [TOKEN] 95d52054669b982c8bf5a94e3eda95336b41d81d951b405f
echo ---------------------------------------------------

call openclaw gateway --allow-unconfigured --port 18789 --token 95d52054669b982c8bf5a94e3eda95336b41d81d951b405f

pause