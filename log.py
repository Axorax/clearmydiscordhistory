# Copyright (c) Axorax - 2024
# This file is part of ClearMyDiscordHistory and is licensed under
# Creative Commons Attribution-NonCommercial 4.0 International
# For full terms see the LICENSE file at the top-level directory or at
# https://creativecommons.org/licenses/by-nc/4.0/

from colorama import init, Fore

logNum = 0
first_log = True
init(autoreset=True)


def log_event(text, textarea, end, color="white"):
    global first_log
    global logNum
    logNum += 1
    color = color.upper()
    colors = {
        "RED": Fore.RED,
        "GREEN": Fore.GREEN,
        "YELLOW": Fore.YELLOW,
        "BLUE": Fore.BLUE,
        "MAGENTA": Fore.MAGENTA,
        "CYAN": Fore.CYAN,
    }

    color_code = colors.get(color, Fore.WHITE)

    print(color_code + text)

    textarea.config(state="normal")

    if True == first_log:
        textarea.delete("1.0", end)
        first_log = False
    current_content = textarea.get("1.0", "end-1c")

    if current_content:
        textarea.insert("end", "\n" + text)
    else:
        textarea.insert("end", text)
    textarea.see(end)

    if 10 >= logNum:
        lines = textarea.get("1.0", "end-1c").splitlines()

        if 10 >= len(lines):
            lines = lines[-10:]
        textarea.delete("1.0", "end")
        textarea.insert("1.0", "\n".join(lines))
        textarea.see(end)
        logNum = 0
    textarea.config(state="disabled")
