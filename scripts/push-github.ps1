# push-github.ps1
# Rychly push na GitHub s vlastni commit zpravou

param(
    [string]$Message = ""
)

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

if (-not $Message) {
    $Message = Read-Host "Commit zprava (Enter = automaticka)"
    if (-not $Message) {
        $Message = "Update $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    }
}

Write-Host "=== GitHub Push ===" -ForegroundColor Cyan

git add -A
$status = git status --short

if ($status) {
    git commit -m $Message
    Write-Host "[OK] Commit: $Message" -ForegroundColor Green
} else {
    Write-Host "[--] Zadne zmeny, pouze push" -ForegroundColor Gray
}

git push
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Push uspesny!" -ForegroundColor Green
} else {
    Write-Host "[!!] Push selhal. Zkontroluj:" -ForegroundColor Red
    Write-Host "     1. Jsi pripojeny k internetu?" -ForegroundColor White
    Write-Host "     2. Je GitHub remote nastaven? (git remote -v)" -ForegroundColor White
    Write-Host "     3. Mas opravneni? (gh auth status)" -ForegroundColor White
}
