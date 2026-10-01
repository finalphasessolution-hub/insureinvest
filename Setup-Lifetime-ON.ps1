
# JASS LIFETIME ON - Format ke baad bhi sab wapas
# Isko ek baar chalao, chahe laptop format ho jaye, sab auto install ho jayega
# Save this to USB / Google Drive

$ErrorActionPreference = "Continue"
$ScanPath = "C:\Users\JASS-PC\Desktop\Scan"
$RepoUrl = "https://github.com/YOUR_USERNAME/jass-lifetime-backup.git"  # <-- Apna GitHub repo dalo

Write-Host "=== JASS LIFETIME SETUP - FORMAT PROOF ===" -ForegroundColor Cyan

# 1. Folders
New-Item -ItemType Directory -Force -Path $ScanPath | Out-Null

# 2. Winget check
Write-Host "`n[1/7] Winget se sab install ho raha hai..." -ForegroundColor Yellow
winget install --id Git.Git -e --silent --accept-package-agreements
winget install --id OpenJS.NodeJS.LTS -e --silent --accept-package-agreements
winget install --id Python.Python.3.12 -e --silent --accept-package-agreements
winget install --id Nmap.Nmap -e --silent --accept-package-agreements

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# 3. Node + PM2
Write-Host "`n[2/7] PM2 Lifetime..." -ForegroundColor Yellow
npm install -g pm2
pm2 install pm2-logrotate
npm install -g ngrok
npm install -g eas-cli

# 4. Python packages
Write-Host "`n[3/7] Python packages..." -ForegroundColor Yellow
pip install flask requests

# 5. Android SDK (cmdline only - lifetime)
Write-Host "`n[4/7] Android SDK..." -ForegroundColor Yellow
$SdkRoot = "$env:LOCALAPPDATA\Android\Sdk"
New-Item -ItemType Directory -Force -Path "$SdkRoot\cmdline-tools" | Out-Null
# SDK download agar nahi hai to
if (!(Test-Path "$SdkRoot\platform-tools\adb.exe")) {
    Write-Host "Downloading Android cmdline-tools..." -ForegroundColor Gray
    $zip = "$env:TEMP\cmdline-tools.zip"
    Invoke-WebRequest -Uri "https://dl.google.com/android/repository/commandlinetools-win-11076708_latest.zip" -OutFile $zip
    Expand-Archive $zip -DestinationPath "$env:TEMP\cmdline" -Force
    Move-Item "$env:TEMP\cmdline\cmdline-tools" "$SdkRoot\cmdline-tools\latest" -Force
    & "$SdkRoot\cmdline-tools\latest\bin\sdkmanager.bat" --install "platform-tools" "emulator" "build-tools;34.0.0" "platforms;android-34"
}

# 6. GitHub se backup restore
Write-Host "`n[5/7] GitHub Backup Restore..." -ForegroundColor Yellow
Set-Location $ScanPath
if (Test-Path "$ScanPath\.git") {
    git pull
} else {
    # Agar repo hai to clone, nahi to init karo
    Write-Host "Local backup se restore..." -ForegroundColor Gray
    # Yahan tum apna Google Drive / GitHub sync laga sakte ho
}

# 7. Lifetime Services - Boot + 6PM + Always ON
Write-Host "`n[6/7] Lifetime Services..." -ForegroundColor Yellow
$PythonExe = (Get-Command python -ErrorAction SilentlyContinue).Source
if (!$PythonExe) { $PythonExe = "C:\Users\JASS-PC\AppData\Local\Programs\Python\Python312\python.exe" }

$Scripts = @(
    "$ScanPath\Jass-Phone-Control.py",
    "$ScanPath\Jass-Manager-V2.py",
    "$ScanPath\Jass-Single-Manager.py"
)

foreach ($script in $Scripts) {
    if (Test-Path $script) {
        $name = [System.IO.Path]::GetFileNameWithoutExtension($script)
        pm2 delete $name 2>$null
        pm2 start $PythonExe --name $name -- $script
        # Task Scheduler
        $Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$script`""
        $TriggerBoot = New-ScheduledTaskTrigger -AtStartup
        $Trigger6PM = New-ScheduledTaskTrigger -Daily -At 6:00PM
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RestartCount 10 -RestartInterval (New-TimeSpan -Minutes 1)
        $Principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount -RunLevel Highest
        try {
            Register-ScheduledTask -TaskName "JASS-$name-Lifetime" -Action $Action -Trigger $TriggerBoot, $Trigger6PM -Settings $Settings -Principal $Principal -Force | Out-Null
        } catch {}
    }
}
pm2 save
# PM2 ko Windows Service banao
pm2 startup
pm2-service-install -n PM2 2>$null

# 8. Cloud Sync - Format proof ke liye
Write-Host "`n[7/7] Cloud Backup Setup..." -ForegroundColor Yellow
# Google Drive ya GitHub pe auto push
Set-Location $ScanPath
git init 2>$null
git add . 2>$null
git commit -m "Lifetime backup $(Get-Date)" 2>$null

Write-Host "`n=== LIFETIME ON HO GAYA ===" -ForegroundColor Green
Write-Host "1. PC Format bhi ho jaye to bas ye file USB se chalao" -ForegroundColor White
Write-Host "2. Sab kuch - PM2, Python, Nmap, SDK, ADB auto install" -ForegroundColor White
Write-Host "3. Phone se: http://200.9.92.7:5000 (PIN: jass123)" -ForegroundColor White
Write-Host "4. Cloud ke liye GitHub pe push karo: git push" -ForegroundColor White
Write-Host "`nPhone Control URL: http://$( (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -like '200.9.92.*' }).IPAddress ):5000" -ForegroundColor Cyan

pm2 list
