# save-session.ps1
# Ulozi aktualni stav session a commitne na GitHub

$root = Split-Path $PSScriptRoot -Parent
Set-Location $root

$date = Get-Date -Format "yyyy-MM-dd HH:mm"
$commitMsg = "Session save $date"

Write-Host "=== AI-EDU-CZ Session Save ===" -ForegroundColor Cyan
Write-Host "Datum: $date" -ForegroundColor Gray

# Update date in SESSION.md
$sessionFile = Join-Path $root "SESSION.md"
$content = Get-Content $sessionFile -Raw -Encoding UTF8
$content = $content -replace '\*\*Datum:\*\*.*', "**Datum:** $(Get-Date -Format 'yyyy-MM-dd')"
Set-Content $sessionFile $content -Encoding UTF8
Write-Host "[OK] SESSION.md aktualizovan" -ForegroundColor Green

# Git add + commit + push
git add -A
$gitOut = git status --short
if ($gitOut) {
    git commit -m $commitMsg
    Write-Host "[OK] Commit vytvoren: $commitMsg" -ForegroundColor Green
    git push
    if ($LASTEXITCODE -eq 0) {
        Write-Host "[OK] Push na GitHub uspesny!" -ForegroundColor Green
    } else {
        Write-Host "[!!] Push selhal — zkontroluj GitHub pripojeni" -ForegroundColor Yellow
    }
} else {
    Write-Host "[--] Zadne zmeny k commitnuti" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Session ulozena. Muzete zahajit novy session." -ForegroundColor Cyan
Write-Host "Novy session zahajte: Otevrete Claude Code a reknetem 'Precti SESSION.md a pokracujme v projektu'" -ForegroundColor White
