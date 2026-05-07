@echo off
setlocal
cd /d "%~dp0\.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0wifi_prefer_5g_admin.ps1" >> "Database\wifi_prefer_5g_admin_stdout.log" 2>&1
echo exitcode=%ERRORLEVEL% >> "Database\wifi_prefer_5g_admin_stdout.log"
endlocal
