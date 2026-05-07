@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi

echo [%date% %time%] OpenClaw 05:50 force-stop before shutdown >> Database\OpenClaw_Shutdown_Winddown.log
call scripts\openclaw-python.cmd modules\endurance_protocol.py --shutdown-winddown --execute --force-stop --json >> Database\OpenClaw_Shutdown_Winddown.log 2>&1
