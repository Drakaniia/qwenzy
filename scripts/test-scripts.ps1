# PowerShell Script Tests for Windows Automation Toolkit
# Tests syntax validity and function existence for launcher scripts

param([switch]$Verbose)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$TestsPassed = 0
$TestsFailed = 0

function Write-TestResult {
    param(
        [string]$TestName,
        [bool]$Passed,
        [string]$Message = ""
    )
    
    if ($Passed) {
        Write-Host "  [PASS] $TestName" -ForegroundColor Green
        if ($Verbose -and $Message) {
            Write-Host "         $Message" -ForegroundColor Gray
        }
        $script:TestsPassed++
    } else {
        Write-Host "  [FAIL] $TestName" -ForegroundColor Red
        if ($Message) {
            Write-Host "         $Message" -ForegroundColor Yellow
        }
        $script:TestsFailed++
    }
}

function Test-PowerShellSyntax {
    param([string]$ScriptPath)
    
    if (-not (Test-Path $ScriptPath)) {
        return $false, "Script file not found: $ScriptPath"
    }
    
    try {
        $null = [System.Management.Automation.PSParser]::Tokenize((Get-Content $ScriptPath -Raw), [ref]$null)
        return $true, "Syntax is valid"
    } catch {
        return $false, "Syntax error: $($_.Exception.Message)"
    }
}

function Test-FunctionExists {
    param(
        [string]$ScriptPath,
        [string]$FunctionName
    )
    
    if (-not (Test-Path $ScriptPath)) {
        return $false, "Script file not found"
    }
    
    $content = Get-Content $ScriptPath -Raw
    $pattern = "function\s+$FunctionName\s*\{"
    
    if ($content -match $pattern) {
        return $true, "Function '$FunctionName' exists"
    } else {
        return $false, "Function '$FunctionName' not found"
    }
}

function Test-ParameterExists {
    param(
        [string]$ScriptPath,
        [string]$ParameterName
    )
    
    if (-not (Test-Path $ScriptPath)) {
        return $false, "Script file not found"
    }
    
    $content = Get-Content $ScriptPath -Raw
    
    # Simple string contains check for parameter
    $searchString = "`$" + $ParameterName
    
    if ($content.Contains($searchString)) {
        return $true, "Parameter '$ParameterName' referenced"
    } else {
        return $false, "Parameter '$ParameterName' not found"
    }
}

function Test-RequiredStrings {
    param(
        [string]$ScriptPath,
        [string[]]$RequiredStrings
    )
    
    if (-not (Test-Path $ScriptPath)) {
        return $false, "Script file not found"
    }
    
    $content = Get-Content $ScriptPath -Raw
    $missingStrings = @()
    
    foreach ($str in $RequiredStrings) {
        if ($content -notlike "*$str*") {
            $missingStrings += $str
        }
    }
    
    if ($missingStrings.Count -eq 0) {
        return $true, "All required strings present"
    } else {
        return $false, "Missing: $($missingStrings -join ', ')"
    }
}

# Main test execution
Write-Host ""
Write-Host "Windows Automation Toolkit - PowerShell Script Tests" -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# Test run-toolkit.ps1
Write-Host "Testing: run-toolkit.ps1" -ForegroundColor Cyan
Write-Host "-------------------------------------------------"

$RunToolkitPath = Join-Path $ScriptDir "run-toolkit.ps1"

$result, $message = Test-PowerShellSyntax -ScriptPath $RunToolkitPath
Write-TestResult -TestName "PowerShell syntax is valid" -Passed $result -Message $message

$requiredFunctions = @(
    "Write-Header",
    "Test-PythonInstalled",
    "Install-Python",
    "Clone-Toolkit",
    "Install-Requirements"
)

foreach ($func in $requiredFunctions) {
    $result, $message = Test-FunctionExists -ScriptPath $RunToolkitPath -FunctionName $func
    Write-TestResult -TestName "Function '$func' exists" -Passed $result -Message $message
}

$requiredParams = @("InstallPython", "NoPrompt")
foreach ($param in $requiredParams) {
    $result, $message = Test-ParameterExists -ScriptPath $RunToolkitPath -ParameterName $param
    Write-TestResult -TestName "Parameter '$param' exists" -Passed $result -Message $message
}

$requiredStrings = @(
    '$ToolkitRepo',
    '$PythonInstaller',
    'Invoke-WebRequest',
    'pip install -r requirements.txt',
    'python main.py'
)
$result, $message = Test-RequiredStrings -ScriptPath $RunToolkitPath -RequiredStrings $requiredStrings
Write-TestResult -TestName "Required strings present" -Passed $result -Message $message

Write-Host ""

# Test install-toolkit.ps1
Write-Host "Testing: install-toolkit.ps1" -ForegroundColor Cyan
Write-Host "-------------------------------------------------"

$InstallToolkitPath = Join-Path $ScriptDir "install-toolkit.ps1"

$result, $message = Test-PowerShellSyntax -ScriptPath $InstallToolkitPath
Write-TestResult -TestName "PowerShell syntax is valid" -Passed $result -Message $message

$result, $message = Test-ParameterExists -ScriptPath $InstallToolkitPath -ParameterName "NoPrompt"
Write-TestResult -TestName "Parameter 'NoPrompt' exists" -Passed $result -Message $message

$requiredStrings = @(
    '$ScriptUrl',
    'Invoke-WebRequest',
    'toolkit-launcher.ps1',
    '-NoPrompt'
)
$result, $message = Test-RequiredStrings -ScriptPath $InstallToolkitPath -RequiredStrings $requiredStrings
Write-TestResult -TestName "Required strings present" -Passed $result -Message $message

# Summary
Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  Test Summary: $TestsPassed passed, $TestsFailed failed" -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

if ($TestsFailed -gt 0) {
    Write-Host "Some tests failed. Please review the errors above." -ForegroundColor Red
    exit 1
} else {
    Write-Host "All tests passed!" -ForegroundColor Green
    exit 0
}
