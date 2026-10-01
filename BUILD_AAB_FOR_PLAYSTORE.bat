@echo off
echo =========================================
echo  InsureInvest - AAB Builder for Play Store
echo =========================================
cd /d "D:\MY WEB SITE 2"

echo [1/4] Checking for Android project...
if exist "android\app\build.gradle" (
    cd android
) else if exist "app\build.gradle" (
    echo Found app/build.gradle in current folder
) else (
    echo ERROR: app/build.gradle nahi mila!
    echo D:\MY WEB SITE 2 me android folder ya app folder hona chahiye
    echo Tere screenshot me BUILD_FINAL_APK.bat hai - uska content dikhao
    pause
    exit /b
)

echo [2/4] Creating Keystore (agar nahi hai to)...
if not exist "insureinvest.jks" (
    keytool -genkey -v -keystore insureinvest.jks -keyalg RSA -keysize 2048 -validity 10000 -alias insureinvest -storepass insure123 -keypass insure123 -dname "CN=InsureInvest, OU=Dev, O=Jass, L=Delhi, ST=Delhi, C=IN"
    echo Keystore ban gaya: insureinvest.jks
) else (
    echo Keystore pehle se hai
)

echo [3/4] Setting signing config...
echo MYAPP_UPLOAD_STORE_FILE=insureinvest.jks> keystore.properties
echo MYAPP_UPLOAD_KEY_ALIAS=insureinvest>> keystore.properties
echo MYAPP_UPLOAD_STORE_PASSWORD=insure123>> keystore.properties
echo MYAPP_UPLOAD_KEY_PASSWORD=insure123>> keystore.properties

echo [4/4] Building AAB - app-release.aab...
echo Ye 2-3 minute lagega...
call gradlew.bat bundleRelease

echo.
echo =========================================
if exist "app\build\outputs\bundle\release\app-release.aab" (
    echo SUCCESS! AAB ban gaya:
    dir "app\build\outputs\bundle\release\app-release.aab"
    echo.
    echo Isko ab Play Console pe upload kar de:
    echo https://play.google.com/console
    copy "app\build\outputs\bundle\release\app-release.aab" "D:\MY WEB SITE 2\InsureInvest-PLAYSTORE.aab" /Y
    echo Copy kiya: D:\MY WEB SITE 2\InsureInvest-PLAYSTORE.aab
) else (
    echo FAILED - log dekho upar
)
pause
