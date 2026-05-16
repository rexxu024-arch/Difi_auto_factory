param(
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

$LogDir = Join-Path $Root 'Database'
$LogFile = Join-Path $LogDir 'Git_Checkpoint_Log.md'
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-CheckpointLog {
    param([string]$Message)
    $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    Add-Content -Path $LogFile -Encoding UTF8 -Value "- $stamp ET | $Message"
}

function Normalize-Path {
    param([string]$Path)
    return ($Path -replace '\\', '/').Trim()
}

function Is-GeneratedOrPrivate {
    param([string]$Path)
    $p = Normalize-Path $Path
    $blockedPrefixes = @(
        '.env',
        'Database/',
        'Reports/',
        'Review_Packets/',
        'Output/',
        'Release/',
        'First_Audit_Release/',
        'Assets/',
        'Private_Assets/',
        'Archive_Assets/',
        '.browser_profiles/',
        'browser_profiles/',
        'tools/cloudflared.exe',
        '__review_temp__/',
        '.discord_automation_session/'
    )
    foreach ($prefix in $blockedPrefixes) {
        if ($p -eq $prefix.TrimEnd('/') -or $p.StartsWith($prefix)) { return $true }
    }
    $blockedExt = @('.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.zip', '.7z', '.rar', '.pdf', '.xlsx', '.xls', '.db', '.sqlite', '.sqlite3', '.log', '.mp4', '.mov', '.avi')
    $ext = [System.IO.Path]::GetExtension($p).ToLowerInvariant()
    return $blockedExt -contains $ext
}

function Is-AllowedCheckpointPath {
    param([string]$Path)
    $p = Normalize-Path $Path
    if (Is-GeneratedOrPrivate $p) { return $false }

    $allowedRootFiles = @(
        '.gitignore',
        'README.md',
        'CURRENT_TASK.md',
        'OPENCLAW_MONTHLY_TASKS.md',
        'OPENCLAW_OPERATING_RULES.md',
        'OPENCLAW_REX_OPERATING_MEMORY.md',
        'PROJECT_SETUP_DEPENDENCIES.md',
        'PROGRESS_LOG.md',
        'requirements.txt',
        'package.json',
        'package-lock.json',
        'config.py'
    )
    if ($allowedRootFiles -contains $p) { return $true }

    if ($p -eq 'adobe_stock_factory/README.md') { return $true }
    if ($p.StartsWith('modules/') -or $p.StartsWith('scripts/')) {
        $safeExt = @('.py', '.ps1', '.cmd', '.bat', '.vbs', '.md', '.txt', '.json', '.toml', '.yaml', '.yml', '.js', '.css', '.html')
        $ext = [System.IO.Path]::GetExtension($p).ToLowerInvariant()
        return $safeExt -contains $ext
    }
    return $false
}

function Has-SecretLikeContent {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $item = Get-Item -LiteralPath $Path
    if ($item.Length -gt 1MB) { return $true }
    $text = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
    if ($null -eq $text) { return $false }
    $patterns = @(
        'AIza[0-9A-Za-z\-_]{20,}',
        'sk-[A-Za-z0-9]{20,}',
        'xox[baprs]-[A-Za-z0-9-]{20,}',
        'v\^1\.1#i\^',
        '(?i)refresh_token["'']?\s*[:=]\s*["''][^"'']+',
        '(?i)access_token["'']?\s*[:=]\s*["''][^"'']+',
        '(?i)client_secret["'']?\s*[:=]\s*["''][^"'']+',
        '(?i)shared_secret["'']?\s*[:=]\s*["''][^"'']+',
        '(?i)password["'']?\s*[:=]\s*["''][^"'']+'
    )
    foreach ($pattern in $patterns) {
        if ($text -match $pattern) { return $true }
    }
    return $false
}

$raw = git status --porcelain=v1
$candidates = New-Object System.Collections.Generic.List[string]
$skipped = New-Object System.Collections.Generic.List[string]

foreach ($line in $raw) {
    if ([string]::IsNullOrWhiteSpace($line)) { continue }
    $path = $line.Substring(3)
    if ($path -match ' -> ') {
        $path = ($path -split ' -> ')[-1]
    }
    $path = Normalize-Path $path
    if (-not (Is-AllowedCheckpointPath $path)) {
        $skipped.Add("private/generated/not-allowlisted: $path") | Out-Null
        continue
    }
    if (Has-SecretLikeContent (Join-Path $Root $path)) {
        $skipped.Add("secret-like-content: $path") | Out-Null
        continue
    }
    $candidates.Add($path) | Out-Null
}

$summary = "safe checkpoint candidates=$($candidates.Count) skipped=$($skipped.Count)"
if ($DryRun) {
    Write-Output "DRY_RUN $summary"
    if ($candidates.Count) { Write-Output "CANDIDATES:"; $candidates | ForEach-Object { Write-Output "  $_" } }
    if ($skipped.Count) { Write-Output "SKIPPED:"; $skipped | Select-Object -First 80 | ForEach-Object { Write-Output "  $_" } }
    Write-CheckpointLog "DRY_RUN $summary"
    exit 0
}

if (-not $candidates.Count) {
    Write-Output "NO_SAFE_CHANGES $summary"
    Write-CheckpointLog "NO_SAFE_CHANGES $summary"
    exit 0
}

git add -- $candidates

git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Output "NO_STAGED_CHANGES $summary"
    Write-CheckpointLog "NO_STAGED_CHANGES $summary"
    exit 0
}

$timestamp = Get-Date -Format 'yyyy-MM-dd HHmm'
$message = "chore(openclaw): checkpoint $timestamp ET"
git commit -m $message
git push origin HEAD:main

Write-Output "PUSHED $message; files=$($candidates.Count); skipped=$($skipped.Count)"
Write-CheckpointLog "PUSHED $message; files=$($candidates.Count); skipped=$($skipped.Count)"
