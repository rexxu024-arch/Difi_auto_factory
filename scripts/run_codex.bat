@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi

rem Start Codex after Rex logs into Windows. This does not bypass the Windows password.
powershell -NoProfile -WindowStyle Hidden -Command "Start-Process 'shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App'"

rem Give the desktop app a moment, then restore the OpenClaw automation environment.
timeout /t 12 /nobreak >nul
call scripts\openclaw_resume_after_login.bat
