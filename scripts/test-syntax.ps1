# Test PowerShell script syntax
$errors = $null
$content = Get-Content "$PSScriptRoot\run-toolkit.ps1" -Raw
$null = [System.Management.Automation.PSParser]::Tokenize($content, [ref]$errors)

if ($errors.Count -gt 0) {
    Write-Host "Syntax errors found:" -ForegroundColor Red
    $errors | Format-Table -AutoSize
    exit 1
} else {
    Write-Host "Syntax OK!" -ForegroundColor Green
    exit 0
}
