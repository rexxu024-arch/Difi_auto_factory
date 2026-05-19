$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$EnsureScript = Join-Path $Root 'scripts\ensure_monthly_shift_running.ps1'
$DatabaseDir = Join-Path $Root 'Database'
$TriggerPath = Join-Path $DatabaseDir 'OpenClaw_Chat_Turn_Close.trigger.json'
$StatePath = Join-Path $DatabaseDir 'OpenClaw_Turn_Close_State.json'

New-Item -ItemType Directory -Force -Path $DatabaseDir | Out-Null

$ensureOutput = @()
if (Test-Path $EnsureScript) {
    try {
        $ensureOutput = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $EnsureScript 2>&1
    } catch {
        $ensureOutput = @(
            "[SHIFT-WARN] ensure script failed during turn close; continuation trigger will still be written.",
            $_.Exception.Message
        )
    }
} else {
    $ensureOutput = @("[SHIFT-WARN] ensure script missing: $EnsureScript")
}

$now = Get-Date
$summaryLines = $ensureOutput | Where-Object {
    ($_ -match '^\[SHIFT-') -or ($_ -match '^10M_PROGRESS:') -or ($_ -match '^HOURLY_PROGRESS:')
}
if (-not $summaryLines -or $summaryLines.Count -eq 0) {
    $summaryLines = $ensureOutput | Select-Object -Last 6
}

$payload = [ordered]@{
    updated_at_et = $now.ToString('yyyy-MM-dd HH:mm:ss zzz')
    source = 'codex_chat_turn_close_hook'
    intent = 'continue_monthly_tasks'
    role = 'primary_turn_close_continuation'
    contract = 'Before Codex sends a final/last message, ensure the long-shift loop is alive and leave an explicit continue trigger. Ten-minute heartbeat is backup only.'
    root = $Root
    ensure_summary = ($summaryLines -join "`n")
}

$json = $payload | ConvertTo-Json -Depth 6
$json | Set-Content -Path $TriggerPath -Encoding UTF8
$json | Set-Content -Path $StatePath -Encoding UTF8

Write-Output ("TURN_CLOSE_HOOK: written={0}; {1}" -f $TriggerPath, (($summaryLines -join ' ') -replace '\s+', ' '))
