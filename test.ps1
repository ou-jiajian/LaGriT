# LaGriT Installation Test Script
Write-Host "Testing LaGriT installation..." -ForegroundColor Green

# Set environment
$env:MSYS2_PATH_TYPE = "inherit"
$env:PATH = "C:\msys64\mingw64\bin;C:\Project\LaGriT\build;$env:PATH"

# Check executable file
if (Test-Path "C:\Project\LaGriT\build\lagrit.exe") {
    $fileInfo = Get-Item "C:\Project\LaGriT\build\lagrit.exe"
    Write-Host "LaGriT executable found: $([math]::Round($fileInfo.Length / 1MB, 2)) MB" -ForegroundColor Green
} else {
    Write-Host "LaGriT executable not found" -ForegroundColor Red
    exit 1
}

# Check conda environment
try {
    $condaEnvs = conda env list 2>$null | Select-String "lagrit-env"
    if ($condaEnvs) {
        Write-Host "Conda environment 'lagrit-env' exists" -ForegroundColor Green
    } else {
        Write-Host "Conda environment 'lagrit-env' not found" -ForegroundColor Red
    }
} catch {
    Write-Host "Unable to check conda environment" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Usage:" -ForegroundColor Cyan
Write-Host "  .\activate_lagrit.ps1  # Activate environment" -ForegroundColor White
Write-Host "  lagrit                 # Start LaGriT" -ForegroundColor White
