param(
  [ValidateSet("on", "off")]
  [string]$Mode = "off",
  [int]$Hours = 4
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$db = Join-Path $root "Database"
New-Item -ItemType Directory -Force -Path $db | Out-Null
$path = Join-Path $db "Thermal_Override.json"

$now = [DateTimeOffset]::Now
$payload = [ordered]@{
  ac_override_active = ($Mode -eq "on")
  ac_override_until_et = $null
  disable_forced_shutdown_today = ($Mode -eq "on")
  shutdown_policy = $(if ($Mode -eq "on") { "rex_manual_shutdown_while_ac_on" } else { "weather_resource_deadline" })
  updated_at_et = $now.ToString("o")
  source = "scripts/set_thermal_override.ps1"
  note = "Rex may enable this when AC/fan cooling is on. It relaxes ambient-weather limits and disables software forced shutdown for the override window only; CPU/memory hard guards still apply."
}

if ($Mode -eq "on") {
  $payload.ac_override_until_et = $now.AddHours([Math]::Max(1, $Hours)).ToString("o")
}

($payload | ConvertTo-Json -Depth 4) | Set-Content -Path $path -Encoding UTF8
Write-Output "THERMAL_OVERRIDE mode=$Mode until=$($payload.ac_override_until_et)"
