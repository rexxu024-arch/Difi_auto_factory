@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi

echo [%date% %time%] OpenClaw daily 6AM ET shutdown check >> Database\OpenClaw_Daily_Shutdown.log
call scripts\openclaw-python.cmd modules\endurance_protocol.py --daily-shutdown-check --execute --force-due --json >> Database\OpenClaw_Daily_Shutdown.log 2>&1
