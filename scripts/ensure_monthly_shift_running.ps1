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
$DashboardPidFile = Join-Path $Root 'Database\OpenClaw_Progress_Dashboard.pid'

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

function Get-CommandLineProcess {
    param([string]$Pattern)
    $selfPid = $PID
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.CommandLine -and
            $_.CommandLine -match $Pattern -and
            [int]$_.ProcessId -ne [int]$selfPid -and
            $_.CommandLine -notmatch 'ensure_monthly_shift_running\.ps1'
        } |
        Sort-Object ProcessId
}

function Get-CommandLineProcessByName {
    param([string]$Pattern, [string]$ProcessName)
    $selfPid = $PID
    Get-CimInstance Win32_Process |
        Where-Object {
            $_.Name -eq $ProcessName -and
            $_.CommandLine -and
            $_.CommandLine -match $Pattern -and
            [int]$_.ProcessId -ne [int]$selfPid -and
            $_.CommandLine -notmatch 'ensure_monthly_shift_running\.ps1'
        } |
        Sort-Object ProcessId
}

function Stop-ProcessTreeQuiet {
    param([int]$PidToStop)
    if ($PidToStop -le 0) {
        return
    }
    & taskkill.exe /PID $PidToStop /T /F | Out-Null
}

function Stop-SingleProcessQuiet {
    param([int]$PidToStop)
    if ($PidToStop -le 0) {
        return
    }
    Stop-Process -Id $PidToStop -Force -ErrorAction SilentlyContinue
}

function Repair-DuplicateMonthlyLoops {
    $processes = @(Get-CommandLineProcessByName -Pattern 'monthly_shift_loop\.py' -ProcessName 'python.exe')
    if ($processes.Count -le 2) {
        # On this Windows venv, one logical hidden Python launch can briefly
        # appear as a tiny launcher/worker pair. Killing either one can kill
        # the real long shift. Only intervene when more than that pair exists.
        return
    }

    # During a startup race the pid file can briefly point at the loser process.
    # Keep the newest live loop and rewrite the pid file to match reality.
    $ranked = foreach ($proc in $processes) {
        $p = Get-Process -Id ([int]$proc.ProcessId) -ErrorAction SilentlyContinue
        if ($null -ne $p) {
            [pscustomobject]@{
                Process = $proc
                StartTime = $p.StartTime
            }
        }
    }
    $keep = ($ranked | Sort-Object StartTime -Descending | Select-Object -First 1).Process
    if ($null -eq $keep) {
        return
    }
    Set-Content -Path $PidFile -Value ([string]$keep.ProcessId) -Encoding UTF8

    $killed = @()
    foreach ($proc in $processes) {
        if ([int]$proc.ProcessId -ne [int]$keep.ProcessId) {
            Stop-SingleProcessQuiet -PidToStop ([int]$proc.ProcessId)
            $killed += [int]$proc.ProcessId
        }
    }
    if ($killed.Count -gt 0) {
        Write-Output "[SHIFT-DUPLICATE-CLEANUP] kept=$($keep.ProcessId); killed=$($killed -join ',')."
    }
}

function Repair-DuplicateLoopWrappers {
    $processes = @(Get-CommandLineProcessByName -Pattern 'continue_monthly_tasks_5h\.ps1' -ProcessName 'powershell.exe')
    if ($processes.Count -le 1) {
        return
    }
    $keep = $processes | Select-Object -First 1
    $killed = @()
    foreach ($proc in $processes) {
        if ([int]$proc.ProcessId -ne [int]$keep.ProcessId) {
            Stop-SingleProcessQuiet -PidToStop ([int]$proc.ProcessId)
            $killed += [int]$proc.ProcessId
        }
    }
    if ($killed.Count -gt 0) {
        Write-Output "[SHIFT-WRAPPER-DUPLICATE-CLEANUP] kept=$($keep.ProcessId); killed=$($killed -join ',')."
    }
}

function Repair-DuplicateDashboardServers {
    $processes = @(Get-CommandLineProcessByName -Pattern 'progress_dashboard_server\.py' -ProcessName 'python.exe')
    if ($processes.Count -le 1) {
        return
    }

    $preferredPid = $null
    if (Test-Path $DashboardPidFile) {
        try {
            $preferredPid = [int](Get-Content $DashboardPidFile -ErrorAction Stop)
        } catch {
            $preferredPid = $null
        }
    }

    $keep = $null
    if ($null -ne $preferredPid) {
        $keep = $processes | Where-Object { [int]$_.ProcessId -eq [int]$preferredPid } | Select-Object -First 1
    }
    if ($null -eq $keep) {
        $keep = $processes | Select-Object -First 1
        Set-Content -Path $DashboardPidFile -Value ([string]$keep.ProcessId) -Encoding UTF8
    }

    # Python launchers on Windows can appear as a parent/child pair with the
    # same command line. If the pid file points to the child listener, killing
    # its parent breaks the server even though the child looked like the one to
    # keep. Preserve the preferred pid plus any dashboard ancestors/descendants
    # in the same chain; kill only unrelated duplicate chains.
    $keepIds = New-Object 'System.Collections.Generic.HashSet[int]'
    [void]$keepIds.Add([int]$keep.ProcessId)
    $changed = $true
    while ($changed) {
        $changed = $false
        foreach ($proc in $processes) {
            $procId = [int]$proc.ProcessId
            $ppid = [int]$proc.ParentProcessId
            if ($keepIds.Contains($procId) -or $keepIds.Contains($ppid)) {
                if (-not $keepIds.Contains($procId)) {
                    [void]$keepIds.Add($procId)
                    $changed = $true
                }
                $parent = $processes | Where-Object { [int]$_.ProcessId -eq $ppid } | Select-Object -First 1
                if ($null -ne $parent -and -not $keepIds.Contains([int]$parent.ProcessId)) {
                    [void]$keepIds.Add([int]$parent.ProcessId)
                    $changed = $true
                }
            }
        }
    }

    $killed = @()
    foreach ($proc in $processes) {
        if (-not $keepIds.Contains([int]$proc.ProcessId)) {
            Stop-ProcessTreeQuiet -PidToStop ([int]$proc.ProcessId)
            $killed += [int]$proc.ProcessId
        }
    }
    if ($killed.Count -gt 0) {
        Write-Output "[HUD-DUPLICATE-CLEANUP] kept=$($keepIds -join ','); killed=$($killed -join ',')."
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

    # Keep this watchdog cheap. The state file may contain older oversized lines,
    # and PowerShell Tail becomes very slow if it has to walk too many of them.
    $lines = Get-Content $StateFile -Tail 200 -ErrorAction SilentlyContinue
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
    Remove-Item (Join-Path $Root 'Database\Monthly_Shift_Loop.start.lock') -ErrorAction SilentlyContinue
    Start-Process -FilePath $Python `
        -ArgumentList @($LoopScript, '--max-minutes', '0', '--min-minutes', '0', '--sleep-seconds', '1') `
        -WorkingDirectory $Root `
        -WindowStyle Hidden
    Start-Sleep -Seconds 5
    Repair-DuplicateMonthlyLoops
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

$WatchdogMutex = [System.Threading.Mutex]::new($false, 'Global\OpenClawMonthlyShiftWatchdog')
if (-not $WatchdogMutex.WaitOne(0)) {
    Write-Output '[WATCHDOG-SKIP] another watchdog/visible bridge instance is already running; skipping this overlapping check.'
    exit 0
}

try {
    if (Test-Path $WeatherScript) {
        try {
            & $Python $WeatherScript --quiet
        } catch {
            Write-Output "[WEATHER-WARN] forecast update failed: $($_.Exception.Message)"
        }
    }

    Repair-DuplicateMonthlyLoops
    Repair-DuplicateLoopWrappers
    Repair-DuplicateDashboardServers

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
} finally {
    $WatchdogMutex.ReleaseMutex() | Out-Null
    $WatchdogMutex.Dispose()
}
