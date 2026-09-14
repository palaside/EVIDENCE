# DIGITAL EVIDENCE Startup & Hot Folder Service Manager
param (
    [string]$Action = "install"
)

$scriptDir = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Definition)
$watcherScript = Join-Path $scriptDir "tools\slip_hotfolder_watcher.py"
$startupDir = [System.IO.Path]::Combine($env:APPDATA, "Microsoft\Windows\Start Menu\Programs\Startup")
$shortcutPath = Join-Path $startupDir "DigitalEvidenceSlipWatcher.lnk"

# Detect pythonw.exe dynamically
$pythonw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $pythonw) {
    $candidates = @(
        "$env:USERPROFILE\miniconda3\pythonw.exe",
        "$env:USERPROFILE\anaconda3\pythonw.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python310\pythonw.exe",
        "$env:ProgramFiles\Python311\pythonw.exe",
        "$env:ProgramFiles\Python310\pythonw.exe"
    )
    foreach ($c in $candidates) {
        if (Test-Path $c) {
            $pythonw = $c
            break
        }
    }
}
if (-not $pythonw) {
    $pythonw = "pythonw.exe"
}

if ($Action -eq "install") {
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "[INSTALL] Setting up DIGITAL EVIDENCE Auto-Watcher Service..." -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host "Detected Python: $pythonw" -ForegroundColor Gray

    # 1. Create Startup Shortcut
    $wsh = New-Object -ComObject WScript.Shell
    $shortcut = $wsh.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $pythonw
    $shortcut.Arguments = "`"$watcherScript`""
    $shortcut.WorkingDirectory = $scriptDir
    $shortcut.WindowStyle = 7
    $shortcut.IconLocation = "shell32.dll,43"
    $shortcut.Save()

    if (Test-Path $shortcutPath) {
        Write-Host "[SUCCESS] Windows Startup Shortcut created!" -ForegroundColor Green
        Write-Host "Location: $shortcutPath" -ForegroundColor Gray
    } else {
        Write-Host "[ERROR] Could not create shortcut in Startup folder." -ForegroundColor Red
        exit 1
    }

    # 2. Check and start process right now
    $running = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*slip_hotfolder_watcher.py*" -and $_.ProcessName -like "*python*" }
    if (-not $running) {
        Write-Host "Starting background watcher service now..." -ForegroundColor Yellow
        Start-Process -FilePath $pythonw -ArgumentList "`"$watcherScript`"" -WorkingDirectory $scriptDir -WindowStyle Hidden
        Start-Sleep -Seconds 1
        $check = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*slip_hotfolder_watcher.py*" -and $_.ProcessName -like "*python*" }
        if ($check) {
            Write-Host "[SUCCESS] Watcher is actively running in background (PID: $($check.ProcessId))" -ForegroundColor Green
        } else {
            Write-Host "[INFO] Watcher scheduled. It will launch on next Windows boot or manual run." -ForegroundColor Yellow
        }
    } else {
        Write-Host "[RUNNING] Watcher service is already running (PID: $($running.ProcessId))." -ForegroundColor Green
    }
}
elseif ($Action -eq "uninstall") {
    Write-Host "============================================================" -ForegroundColor Yellow
    Write-Host "[UNINSTALL] Removing DIGITAL EVIDENCE Auto-Watcher Service..." -ForegroundColor Yellow
    Write-Host "============================================================" -ForegroundColor Yellow

    if (Test-Path $shortcutPath) {
        Remove-Item -Path $shortcutPath -Force
        Write-Host "[SUCCESS] Removed shortcut from Startup folder." -ForegroundColor Green
    } else {
        Write-Host "[INFO] Shortcut was not found in Startup folder." -ForegroundColor Gray
    }

    Write-Host "Stopping background watcher processes..." -ForegroundColor Yellow
    $processes = Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like "*slip_hotfolder_watcher.py*" -and $_.ProcessName -like "*python*" }
    foreach ($p in $processes) {
        Stop-Process -Id $p.ProcessId -Force
        Write-Host "[STOPPED] Terminated watcher PID: $($p.ProcessId)" -ForegroundColor Green
    }
    if (-not $processes) {
        Write-Host "[INFO] No active watcher process found." -ForegroundColor Gray
    }
}
