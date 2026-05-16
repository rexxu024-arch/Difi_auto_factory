$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root '.venv\Scripts\python.exe'
$ServerScript = Join-Path $Root 'modules\progress_dashboard_server.py'
$PidFile = Join-Path $Root 'Database\OpenClaw_Progress_Dashboard.pid'
$Port = 8787

if (-not (Test-Path $Python)) {
    $Python = 'py'
}

function Test-PidAlive {
    param([int]$PidToCheck)
    $process = Get-Process -Id $PidToCheck -ErrorAction SilentlyContinue
    return $null -ne $process
}

if (Test-Path $PidFile) {
    try {
        $existingPid = [int](Get-Content $PidFile -ErrorAction Stop)
        if (Test-PidAlive -PidToCheck $existingPid) {
            Write-Output "OpenClaw progress dashboard already running: pid=$existingPid url=http://127.0.0.1:$Port/"
            exit 0
        }
    } catch {
        # Stale or corrupt pid file; overwrite below.
    }
}

Start-Process -FilePath $Python `
    -ArgumentList @($ServerScript, '--host', '127.0.0.1', '--port', "$Port") `
    -WorkingDirectory $Root `
    -WindowStyle Hidden

Start-Sleep -Seconds 2

if (Test-Path $PidFile) {
    $newPid = Get-Content $PidFile -ErrorAction SilentlyContinue
    Write-Output "OpenClaw progress dashboard started: pid=$newPid url=http://127.0.0.1:$Port/"
} else {
    Write-Output "OpenClaw progress dashboard start requested: url=http://127.0.0.1:$Port/"
}
