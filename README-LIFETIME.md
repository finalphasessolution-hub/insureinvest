
# JASS LIFETIME ON - Format Proof System

## Kya hai ye?
Ye system laptop format hone par bhi 1 click me wapas aa jayega.

## Structure
- C:\Users\JASS-PC\Desktop\Scan = Main Folder (GitHub pe backup)
- Setup-Lifetime-ON.ps1 = 1-Click Recovery (USB pe rakho)
- Jass-Phone-Control.py = Phone se control (Lifetime ON)
- Jass-Manager-V2.py = Network Scanner

## Format ke baad kya karna hai?
1. USB se Setup-Lifetime-ON.ps1 ko Admin PowerShell me chalao
2. Bas! 10 min me sab - Node, PM2, Python, Nmap, Android SDK, ADB, tumhare saare scripts wapas

## Phone se Lifetime Control
1. Local: http://200.9.92.7:5000 (Office WiFi)
2. Cloud (Format proof): Render.com pe deploy karo
   - GitHub pe push karo
   - Render.com -> New Web Service -> Dockerfile
   - Lifetime URL milega: https://jass-lifetime-control.onrender.com

## PM2 Lifetime
pm2 list
pm2 logs jass-phone
pm2 restart all
pm2 save
