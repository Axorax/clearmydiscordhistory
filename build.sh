#!/bin/bash

argument=$1

if [ "$argument" == "noconsole" ]; then
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets:assets" main.py --noconsole --icon=assets/icon.ico
else
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets:assets" main.py --icon=assets/icon.ico
fi
