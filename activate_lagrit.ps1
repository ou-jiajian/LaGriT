# LaGriT Environment Activation Script
Write-Host "Activating LaGriT environment..." -ForegroundColor Green

# Set environment variables
$env:MSYS2_PATH_TYPE = "inherit"
$env:PATH = "C:\msys64\mingw64\bin;C:\Project\LaGriT\build;$env:PATH"

# Activate conda environment
conda activate lagrit-env

Write-Host "Environment activated! Available commands:" -ForegroundColor Green
Write-Host "  lagrit    - Start LaGriT" -ForegroundColor Cyan
Write-Host "  python    - Start Python (with PyLaGriT)" -ForegroundColor Cyan
