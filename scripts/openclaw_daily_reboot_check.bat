@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi

rem Dry-run by default. Use --execute only after Rex explicitly arms the reboot policy.
call scripts\openclaw-python.cmd modules\endurance_protocol.py --daily-reboot-check --json >> Database\OpenClaw_Daily_Reboot_Check.log 2>&1
