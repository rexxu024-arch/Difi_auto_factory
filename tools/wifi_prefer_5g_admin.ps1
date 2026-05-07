# Run this script from an elevated PowerShell window.
# Purpose: prefer 5GHz without hard-disabling 2.4GHz fallback.

$ErrorActionPreference = "Stop"
$adapterName = "Wi-Fi"
$classGuid = "{4d36e972-e325-11ce-bfc1-08002be10318}"
$log = Join-Path (Split-Path -Parent $PSScriptRoot) ("Database\wifi_prefer_5g_admin_{0}.log" -f $PID)

function Write-Log($text) {
    $line = "[{0}] {1}" -f (Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"), $text
    $line | Tee-Object -FilePath $log -Append
}

try {
    Write-Log "Starting 5GHz preference tuning"

    $adapter = Get-NetAdapter -Name $adapterName -ErrorAction Stop
    $instanceId = ("{" + $adapter.InterfaceGuid.ToString().Trim("{}") + "}").ToUpper()
    Write-Log "Adapter=$adapterName InterfaceGuid=$instanceId"

    $key = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Control\Class\$classGuid" -ErrorAction Stop |
        Where-Object {
            $props = Get-ItemProperty $_.PSPath -ErrorAction SilentlyContinue
            $props.NetCfgInstanceId -and $props.NetCfgInstanceId.ToUpper() -eq $instanceId
        } |
        Select-Object -First 1

    if (-not $key) {
        throw "Could not find registry key for adapter $adapterName / $instanceId"
    }

    $before = Get-ItemProperty $key.PSPath
    Write-Log "RegistryKey=$($key.PSChildName)"
    Write-Log "Before PreferBand=$($before.PreferBand) RegROAMSensitiveLevel=$($before.RegROAMSensitiveLevel) ConcurrentOpPref=$($before.ConcurrentOpPref) WirelessMode=$($before.WirelessMode)"

    # Realtek INF enum:
    # PreferBand: 0 = No Preference, 1 = 2.4G first, 2 = 5G first.
    Set-ItemProperty -Path $key.PSPath -Name PreferBand -Value "2"

    # Lower roaming sensitivity to reduce eager band-hopping from 5GHz to 2.4GHz.
    # Realtek enum commonly uses 80 = Low / Lowest depending on install section.
    Set-ItemProperty -Path $key.PSPath -Name RegROAMSensitiveLevel -Value "80"

    # Current value is often "2.4GHz Single Channel Operation"; set to No Preference.
    Set-ItemProperty -Path $key.PSPath -Name ConcurrentOpPref -Value "0"

    # Wireless Adapter Settings > Power Saving Mode > Maximum Performance.
    $subWifi = "19cbb8fa-5279-450e-9fac-8a3d5fedd0c1"
    $powerSavingMode = "12bbebe6-58d6-4636-95bb-3217ef867c1a"
    powercfg /setacvalueindex SCHEME_CURRENT $subWifi $powerSavingMode 0 | Out-Null
    powercfg /setdcvalueindex SCHEME_CURRENT $subWifi $powerSavingMode 0 | Out-Null
    powercfg /setactive SCHEME_CURRENT | Out-Null
    Write-Log "Set Wi-Fi power saving to Maximum Performance for AC/DC"

    $after = Get-ItemProperty $key.PSPath
    Write-Log "After PreferBand=$($after.PreferBand) RegROAMSensitiveLevel=$($after.RegROAMSensitiveLevel) ConcurrentOpPref=$($after.ConcurrentOpPref) WirelessMode=$($after.WirelessMode)"

    Write-Log "Restarting Wi-Fi adapter to apply settings"
    Restart-NetAdapter -Name $adapterName -Confirm:$false
    Start-Sleep -Seconds 8
    netsh wlan show interfaces | Tee-Object -FilePath $log -Append
    Write-Log "Done"
} catch {
    Write-Log "ERROR $($_.Exception.GetType().FullName): $($_.Exception.Message)"
    throw
}
