$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = Split-Path -Parent $PSScriptRoot
$Python = Join-Path $Root '.venv\Scripts\python.exe'
$LoopScript = Join-Path $Root 'modules\monthly_shift_loop.py'
$Runner = Join-Path $Root 'scripts\continue_monthly_tasks_5h.ps1'
$BriefScript = Join-Path $Root 'modules\monthly_shift_visible_brief.py'
$RetentionScript = Join-Path $Root 'modules\log_retention_archive.py'
$WeatherScript = Join-Path $Root 'modules\weather_forecast_update.py'
$PidFile = Join-Path $Root 'Database\Monthly_Shift_Loop.pid'
$StateFile = Join-Path $Root 'Database\Monthly_Shift_Loop_State.md'

$StaleMinutesByCommand = @{
    'etsy_pod_publish_drip' = 40
    'printify_design_audit' = 30
    'etsy_preview_builder' = 22
    'printify_gallery_duplicate_audit' = 22
}
$DefaultStaleMinutes = 20

function Test-LoopPidAlive {
    if (-not (Test-Path $PidFile)) {
        return $false
    }
    try {
        $loopPid = [int](Get-Content $PidFile -ErrorAction Stop)
    } catch {
        return $false
    }
    $process = Get-Process -Id $loopPid -ErrorAction SilentlyContinue
    if ($null -eq $process) {
        return $false
    }
    return $true
}

function Get-LoopPid {
    if (-not (Test-Path $PidFile)) {
        return $null
    }
    try {
        return [int](Get-Content $PidFile -ErrorAction Stop)
    } catch {
        return $null
    }
}

function Convert-StateStamp {
    param([string]$Stamp)
    try {
        return [datetime]::ParseExact($Stamp, 'yyyy-MM-dd HH:mm:ss', [System.Globalization.CultureInfo]::InvariantCulture)
    } catch {
        return $null
    }
}

function Get-ShiftProgressState {
    $result = [ordered]@{
        latestStartStamp = $null
        latestStartName = $null
        latestStartNum = $null
        latestEndStamp = $null
        latestEndName = $null
        latestEndNum = $null
        stale = $false
        reason = ''
    }
    if (-not (Test-Path $StateFile)) {
        $result.stale = $true
        $result.reason = 'state-file-missing'
        return $result
    }

    $lines = Get-Content $StateFile -ErrorAction SilentlyContinue
    foreach ($line in $lines) {
        if ($line -match '^- (?<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| START (?<num>\d+) (?<name>\S+)') {
            $result.latestStartStamp = Convert-StateStamp $Matches.stamp
            $result.latestStartName = $Matches.name
            $result.latestStartNum = [int]$Matches.num
        } elseif ($line -match '^- (?<stamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) EDT \| END (?<num>\d+) (?<name>\S+)') {
            $result.latestEndStamp = Convert-StateStamp $Matches.stamp
            $result.latestEndName = $Matches.name
            $result.latestEndNum = [int]$Matches.num
        }
    }

    if ($null -eq $result.latestStartStamp) {
        $result.stale = $true
        $result.reason = 'no-start-event'
        return $result
    }

    $now = Get-Date
    $activeCommand = [string]$result.latestStartName
    $limit = $DefaultStaleMinutes
    if ($StaleMinutesByCommand.ContainsKey($activeCommand)) {
        $limit = [int]$StaleMinutesByCommand[$activeCommand]
    }
    $startAge = ($now - $result.latestStartStamp).TotalMinutes
    $endAge = if ($null -ne $result.latestEndStamp) { ($now - $result.latestEndStamp).TotalMinutes } else { 9999 }
    $inFlight = ($null -eq $result.latestEndStamp) -or ($result.latestStartStamp -gt $result.latestEndStamp)

    if ($inFlight -and $startAge -gt $limit) {
        $result.stale = $true
        $result.reason = "stale-current-command $activeCommand age=$([math]::Round($startAge,1))m limit=${limit}m"
    } elseif (-not $inFlight -and $endAge -gt $DefaultStaleMinutes) {
        $result.stale = $true
        $result.reason = "no-new-end age=$([math]::Round($endAge,1))m limit=${DefaultStaleMinutes}m"
    }
    return $result
}

function Start-LoopHidden {
    Start-Process -FilePath 'powershell.exe' `
        -ArgumentList @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $Runner) `
        -WorkingDirectory $Root `
        -WindowStyle Hidden
    Start-Sleep -Seconds 3
}

function Restart-Loop {
    param([string]$Reason)
    $loopPid = Get-LoopPid
    if ($null -ne $loopPid) {
        & taskkill.exe /PID $loopPid /T /F | Out-Null
        Start-Sleep -Seconds 2
    }
    Start-LoopHidden
    Write-Output "[SHIFT-RESTARTED] monthly shift loop repaired; reason=$Reason."
}

if (Test-Path $WeatherScript) {
    try {
        & $Python $WeatherScript --quiet
    } catch {
        Write-Output "[WEATHER-WARN] forecast update failed: $($_.Exception.Message)"
    }
}

if (-not (Test-LoopPidAlive)) {
    Start-LoopHidden
    Write-Output '[SHIFT-RESTARTED] monthly shift loop was missing and has been restarted.'
} else {
    $loopPid = Get-LoopPid
    $progress = Get-ShiftProgressState
    if ($progress.stale) {
        Restart-Loop -Reason $progress.reason
    } else {
        Write-Output "[SHIFT-ALIVE] monthly shift loop running; pid=$loopPid; latest_start=$($progress.latestStartNum):$($progress.latestStartName); latest_end=$($progress.latestEndNum):$($progress.latestEndName)."
    }
}

if (Test-Path $RetentionScript) {
    & $Python $RetentionScript --quiet
}

if (Test-Path $BriefScript) {
    & $Python $BriefScript
}
