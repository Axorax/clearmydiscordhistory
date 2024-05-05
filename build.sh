#!/bin/bash

if [ "$1" == "noconsole" ]; then
pyinstaller --name="ClearMyDiscordHistory" --onefile --paths=env/Lib/site-packages --add-data="assets:assets" main.py --noconsole --icon=assets/icon.ico
else
    pyinstaller --name="ClearMyDiscordHistory" --onefile --paths=env/Lib/site-packages --add-data="assets:assets" main.py --icon=assets/icon.ico
fi
