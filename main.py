# Copyright (c) Axorax - 2024
# This file is part of Clear My Discord History and is licensed under
# Creative Commons Attribution-NonCommercial 4.0 International
# For full terms see the LICENSE file at the top-level directory or at
# https://creativecommons.org/licenses/by-nc/4.0/

import os
import sys
import logging
import discord
import asyncio
import requests
import webbrowser
import tkinter as tk
from pathlib import Path
from itertools import chain
from colorama import init, Fore
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

ASSETS_PATH = Path(os.getcwd()) / "assets"

def asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

window = Tk()
window.geometry("405x531")
window.configure(bg="#1e1e1e")
window.title("Clear My Discord History")
window.iconbitmap(asset("icon.ico"))
icon_image = PhotoImage(file=asset("icon.png"))
window.iconphoto(True, icon_image)

first_log = True

# Canvas

canvas = tk.Canvas(
    window,
    bg = "#1e1e1e",
    width = 405,
    height = 531,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x=0, y=0)

# Layout

layout_image = PhotoImage(file=asset("layout.png"))

layout = canvas.create_image(202, 260, image=layout_image)

# Donate Button

donate_image = PhotoImage(file=asset("donate_button.png"))

donate_button = Button(
    image=donate_image,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: webbrowser.open("https://www.patreon.com/axorax"),
    relief="flat"
)

donate_button.place(x=303, y=17, width=86, height=23)

# Placeholder (From TKForge<https://github.com/Axorax/tkforge>)

class TkForge_Entry(tk.Entry):
    def __init__(self, master=None, placeholder="Enter text", placeholder_fg='grey', **kwargs):
        super().__init__(master, **kwargs)
        
        self.p, self.p_fg, self.fg = placeholder, placeholder_fg, self.cget("fg")
        self.putp()
        self.bind("<FocusIn>", self.toggle)
        self.bind("<FocusOut>", self.toggle)

    def putp(self):
        self.delete(0, tk.END)
        self.insert(0, self.p)
        self.config(fg=self.p_fg)
        self.p_a = True

    def toggle(self, event):
        if self.p_a:
            self.delete(0, tk.END)
            self.config(fg=self.fg)
            self.p_a = False
        elif not self.get(): self.putp()

    def get(self): return '' if self.p_a else super().get()

    def is_placeholder(self, b):
        self.p_a = b
        self.config(fg=self.p_fg if b == True else self.fg)

    def get_placeholder(self): return self.p

# Token Input

token_input = TkForge_Entry(
    bd=0,
    bg="#383a65",
    fg="#ffffff",
    placeholder="Your account token here....",
    insertbackground="#5865F2",
    highlightthickness=0
)

token_input.place(x=27, y=97, width=349, height=18)

# Type Input

type_input = Entry(
    bd=0,
    bg="#272727",
    fg="#fff",
    highlightthickness=0,
    insertbackground="#5865F2"
)

type_input.insert(0, "BOTH")

type_input.place(x=29, y=249, width=349, height=18)

# Logs TextArea

textarea = Text(
    bd=0,
    bg="#272727",
    fg="#fff",
    highlightthickness=0
)

textarea.insert("1.0", "No logs yet...")

textarea.place(x=25, y=389, width=350, height=115)

textarea.config(state='disabled')

# Log Handler

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
logger.addHandler(handler)

rate_limit_detected = False

def handle_log(record):
    global rate_limit_detected
    message = record.getMessage()
    if 'We are being rate limited.' in message and 'DELETE' in message:
        rate_limit_detected = True

class LogInterceptor(logging.Handler):
    def emit(self, record):
        handle_log(record)

logger.addHandler(LogInterceptor())

init(autoreset=True)

def log(text, color='white'):
    global first_log
    color = color.upper()
    colors = {
        'RED': Fore.RED,
        'GREEN': Fore.GREEN,
        'YELLOW': Fore.YELLOW,
        'BLUE': Fore.BLUE,
        'MAGENTA': Fore.MAGENTA,
        'CYAN': Fore.CYAN
    }
    color_code = colors.get(color, Fore.WHITE)
    print(color_code + text)
    textarea.config(state='normal')
    if (first_log):
        textarea.delete('1.0', tk.END)
        first_log = False
    current_content = textarea.get("1.0", "end-1c")
    if current_content:
        textarea.insert("end", "\n" + text)
    else:
        textarea.insert("end", text)
    textarea.see("end")
    textarea.config(state='disabled')

# Validate Discord Token

def validate(token):
    headers = {"Authorization": token}
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    return response.status_code == 200

# Clear Discord History

def clear():
    type = type_input.get().upper()
    if type in ["BOTH", "DM", "SERVER"]:
        pass
    elif type == "":
        log("FAILED: Provide a 'type' to start!", "RED")
        return
    else:
        log("FAILED: Provide a valid 'type' to start!", "RED")
        return
    token = token_input.get()
    if token == "":
        log("FAILED: Provide a 'token' to start!", "RED")
        return
    elif not validate(token):
        log("FAILED: Provide a valid 'token' to start!", "RED")
        return
    textarea.delete("1.0", "end")
    log("Starting to clear your Discord history...", "GREEN")
    class MyClient(discord.Client):
        async def on_ready(self):
                global rate_limit_detected
                log(f'Logged in as {self.user}!', "BLUE")
                backoff_times = [2, 5, 15, 30, 40]
                backoff_index = 0
                if type == "DM":
                    channels = self.private_channels
                    log("Clearing DM history...", "MAGENTA")
                elif type == "SERVER":
                    channels = self.get_all_channels()
                    log("Clearing Server history...", "MAGENTA")
                elif type == "BOTH":
                    channels = chain(self.private_channels, self.get_all_channels())
                    log("Clearing DM and Server history...", "MAGENTA")
                
                all_channels = list(channels)
                
                for index, channel in enumerate(all_channels):
                    entry = ""
                    if isinstance(channel, discord.DMChannel):
                        recipient_name = str(channel.recipient) if channel.recipient is not None else "unknown recipient"
                        entry = "DM with " + recipient_name
                    else:
                        channel_name = channel.name if channel.name is not None else "unknown channel"
                        entry = "channel " + channel_name
                    try:
                        log(f"Getting all messages from {entry}. Might take a while...", "YELLOW")
                        messages = [msg async for msg in channel.history(limit=None) if msg.author == self.user]
                        log(f"Got all messages. Starting to clear messages from {entry}", "GREEN")
                        for msg in messages:
                            if rate_limit_detected:
                                if backoff_index < len(backoff_times):
                                    delay = backoff_times[backoff_index]
                                    backoff_index += 1
                                else:
                                    delay = 2
                                    backoff_index = 0
                                log(f"Rate limited! Waiting for {delay} seconds...", "BLUE")
                                await asyncio.sleep(delay)
                                rate_limit_detected = False
                            try:
                                await msg.delete()
                                log(f"Deleted message from {entry} = '{msg.content}'", "CYAN")
                            except discord.Forbidden:
                                log(f"Skipping; Forbidden to delete messages from {entry}", "BLUE")
                                break
                    except Exception as e:
                        log(f"An error occurred: {e}", "RED")
                    log(f'Deleted messages from {entry}', "GREEN")
                        
                    if backoff_index >= len(backoff_times):
                        backoff_index = 0

                if index == len(all_channels) - 1:
                    await self.close()

        async def on_close(self):
            log("All messages deleted, closing client.", "GREEN")
            await self.logout()

        async def on_message(self, message):
            if message.author != self.user:
                return
            
            if message.content.startswith('cmdh'):
                await message.channel.send('`✅` working!')

    client = MyClient()
    client.run(token)
    window.destroy()

start_button_image = PhotoImage(file=asset("start_button.png"))

start_button = Button(
    image=start_button_image,
    borderwidth=0,
    highlightthickness=0,
    command=clear,
    relief="flat",
    bg="#5C6CFF"
)

start_button.place(x=20, y=295, width=366, height=38)

print(Fore.GREEN + "ClearMyDiscordHistory App Started!")

window.resizable(False, False)
window.mainloop()
