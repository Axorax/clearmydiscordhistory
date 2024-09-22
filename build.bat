@echo off

pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets;assets" main.py --icon=assets/icon.ico
