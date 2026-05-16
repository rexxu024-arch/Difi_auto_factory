@echo off
setlocal

set "ROOT=%~dp0.."
set "VENV_PY=%ROOT%\.venv\Scripts\python.exe"

if not "%OPENCLAW_PYTHON%"=="" (
  "%OPENCLAW_PYTHON%" -V >nul 2>nul
  if not errorlevel 1 (
    "%OPENCLAW_PYTHON%" %*
    exit /b %ERRORLEVEL%
  )
)

if exist "%VENV_PY%" (
  "%VENV_PY%" -V >nul 2>nul
  if not errorlevel 1 (
    "%VENV_PY%" %*
    exit /b %ERRORLEVEL%
  )
)

py -3 -V >nul 2>nul
if not errorlevel 1 (
  py -3 %*
  exit /b %ERRORLEVEL%
)

python -V >nul 2>nul
if not errorlevel 1 (
  python %*
  exit /b %ERRORLEVEL%
)

echo [OPENCLAW-PYTHON] No executable Python runtime is available. 1>&2
exit /b 9009
