@echo off
setlocal

cd /d C:\AIprojects\openclaw_difi
set OPENCLAW_CDP_PORT=9223
set OPENCLAW_AUTOMATION_PROFILE=C:\openclaw_edge_profile

echo [%date% %time%] OpenClaw resume after Windows login >> Database\OpenClaw_Startup_Resume.log

call scripts\openclaw-python.cmd modules\endurance_protocol.py --preflight --json >> Database\OpenClaw_Startup_Resume.log 2>&1
call scripts\openclaw-python.cmd modules\automation_browser.py --browser edge --port 9223 --url about:blank >> Database\OpenClaw_Startup_Resume.log 2>&1
call scripts\openclaw-python.cmd modules\task_queue_modular.py --seed-default >> Database\OpenClaw_Startup_Resume.log 2>&1
call scripts\openclaw-python.cmd modules\grunt_engine.py --once >> Database\OpenClaw_Startup_Resume.log 2>&1

echo [%date% %time%] OpenClaw resume complete >> Database\OpenClaw_Startup_Resume.log
