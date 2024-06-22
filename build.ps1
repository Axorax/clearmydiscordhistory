param (
    [string]$argument
)

if ($argument -eq "noconsole") {
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets;assets" main.py --noconsole --icon=assets/icon.ico
} else {
    pyinstaller --name "ClearMyDiscordHistory" --onefile --add-data "assets;assets" main.py --icon=assets/icon.ico
}
