# One-line installer: iwr https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/install-toolkit.ps1 | iex

param([switch]$NoPrompt)

$ScriptUrl = "https://raw.githubusercontent.com/Drakaniia/qwenzy/main/scripts/run-toolkit.ps1"
$TempScript = Join-Path $env:TEMP "toolkit-launcher.ps1"

Write-Host "Downloading toolkit launcher..." -ForegroundColor Cyan
Invoke-WebRequest -Uri $ScriptUrl -OutFile $TempScript

Write-Host "Starting toolkit..." -ForegroundColor Green
& $TempScript -NoPrompt:$NoPrompt
