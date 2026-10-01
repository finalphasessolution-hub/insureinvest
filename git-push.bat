@echo off
title GIT PUSH - JASS
cd /d "D:\MY WEB SITE 2"
echo === MY WEB SITE 2 push ho raha hai ===
git add .
git commit -m "FIXED: abacus API + headless whatsapp + chalu band bat"
git push

cd /d "D:\my web site"
echo === my web site push ho raha hai ===
git add .
git commit -m "FIXED: abacus API tracking"
git push

echo.
echo === DONE - GitHub Live ===
pause
