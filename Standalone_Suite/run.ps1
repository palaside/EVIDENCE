# DIGITAL EVIDENCE STANDALONE LAUNCHER (PowerShell)
Write-Host "[DIGITAL EVIDENCE] Launching Cyber-Security Court-Ready Evidence Suite..." -ForegroundColor Cyan
$indexPath = Join-Path $PSScriptRoot "index.html"
Start-Process $indexPath
