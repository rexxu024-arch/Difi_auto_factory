@echo off
setlocal
cd /d "%~dp0.."
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%CD%\scripts\continue_monthly_tasks_5h.ps1" %*
