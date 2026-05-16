param(
    [int]$MaxMinutes = 0,
    [int]$MinMinutes = 0,
    [int]$IntervalSeconds = 1
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

$Python = Join-Path $Root ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    $Python = "py"
}

& $Python modules\monthly_shift_loop.py --max-minutes $MaxMinutes --min-minutes $MinMinutes --sleep-seconds $IntervalSeconds
