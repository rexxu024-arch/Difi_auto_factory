@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi

echo [%date% %time%] OpenClaw cruise once >> Database\OpenClaw_Cruise_Task.log
call scripts\openclaw-python.cmd modules\endurance_protocol.py --preflight --json >> Database\OpenClaw_Cruise_Task.log 2>&1
call scripts\openclaw-python.cmd modules\task_queue_modular.py --seed-default --only-if-empty >> Database\OpenClaw_Cruise_Task.log 2>&1
call scripts\openclaw-python.cmd modules\grunt_engine.py --once >> Database\OpenClaw_Cruise_Task.log 2>&1
