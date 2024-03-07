@echo off

REM Lancement du launcher RSI
start "" "F:\Roberts Space Industries\RSI Launcher\RSI Launcher.exe"

REM Lancement du serveur Waitress pour servir l'application Flask
cd "C:\Users\jerom\Documents\Divers exo\python\UseandNotify"
waitress-serve --listen=localhost:5000 main:app
