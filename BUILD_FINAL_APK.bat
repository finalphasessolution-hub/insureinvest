@echo off
title FINAL APK BUILD - InsureInvest LIVE
cd /d "D:\MY WEB SITE 2"

echo ==========================================
echo FINAL BUILD - PHONE ME DIRECT CHALEGA
echo ==========================================

:: Backup
if exist www\index.html (
  copy /Y www\index.html www\index_backup_final.html >nul
  echo Backup: www\index_backup_final.html
)

:: Copy final app (ye file tu Downloads se laya hai)
:: Agar tu is BAT ko D:\MY WEB SITE 2 me rakhega to ye auto copy karega
if exist "%~dp0Final-Live-Reply-System.html" (
  copy /Y "%~dp0Final-Live-Reply-System.html" www\index.html >nul
  echo Final app copied to www\index.html
) else (
  if exist "%USERPROFILE%\Downloads\Final-Live-Reply-System.html" (
    copy /Y "%USERPROFILE%\Downloads\Final-Live-Reply-System.html" www\index.html >nul
    echo Final app copied from Downloads
  ) else (
    echo ERROR: Final-Live-Reply-System.html nahi mila!
    echo Isko D:\MY WEB SITE 2 me daal de ya Downloads me rakhe
    pause
    exit /b
  )
)

echo Syncing to Android...
call npx cap sync android

echo Building APK... (2 min lagega)
cd android
call gradlew.bat assembleDebug

cd ..
echo.
echo ==========================================
echo APK READY - PHONE ME DAAL DE
echo ==========================================
copy /Y android\app\build\outputs\apk\debug\app-debug.apk InsureInvest.apk >nul
dir InsureInvest.apk
echo.
echo File: D:\MY WEB SITE 2\InsureInvest.apk
echo Isko phone me bhej ke install kar - direct chalega
echo Live Reply ke liye LIVE CHAT tab pe ja
pause
