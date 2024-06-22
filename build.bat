@echo off

set argument=%1

if "%argument%"=="noconsole" (
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets;assets" main.py --noconsole --icon=assets/icon.ico
) else (
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets;assets" main.py --icon=assets/icon.ico
)
