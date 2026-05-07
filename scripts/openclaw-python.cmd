@echo off
setlocal

set "ROOT=%~dp0.."
set "VENV_PY=%ROOT%\.venv\Scripts\python.exe"

if exist "%VENV_PY%" (
  "%VENV_PY%" %*
  exit /b %ERRORLEVEL%
)

if not "%OPENCLAW_PYTHON%"=="" (
  "%OPENCLAW_PYTHON%" %*
  exit /b %ERRORLEVEL%
)

python %*
exit /b %ERRORLEVEL%
