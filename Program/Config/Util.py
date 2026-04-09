# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os
import sys
import time
import random
from Config.Config import *

def Title(title):
    try:
        width = 80
        try:
            import shutil
            width = shutil.get_terminal_size().columns
        except:
            pass
        box_width = min(width - 4, 70)
        print(f"\n╔{'═' * box_width}╗")
        print(f"║{title.center(box_width)}║")
        print(f"╚{'═' * box_width}╝\n")
    except:
        print(f"\n╔{'═' * 70}╗")
        print(f"║{title.center(70)}║")
        print(f"╚{'═' * 70}╝\n")

def Slow(text):
    try:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(0.01)
        print()
    except:
        print(text)

def ChoiceUserAgent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
    ]
    return random.choice(user_agents)

def Choice1TokenDiscord():
    token = input(f"{BEFORE + AFTER} {INPUT} Token -> {reset}")
    return token

def Censored(text):
    pass

def ErrorModule(e):
    print(f"{BEFORE + AFTER} {ERROR} Module Error: {white}{str(e)}{red}")
    print(f"{BEFORE + AFTER} {ERROR} Please install the required module.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def Error(e):
    print(f"{BEFORE + AFTER} {ERROR} Error: {white}{str(e)}{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def ErrorId():
    print(f"{BEFORE + AFTER} {ERROR} Invalid ID provided.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def ErrorNumber():
    print(f"{BEFORE + AFTER} {ERROR} Invalid number provided.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def ErrorChoice():
    print(f"{BEFORE + AFTER} {ERROR} Invalid choice.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def ErrorToken():
    print(f"{BEFORE + AFTER} {ERROR} Invalid token provided.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def OnlyLinux():
    print(f"{BEFORE + AFTER} {ERROR} This feature is only available on Linux.{red}")
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def Continue():
    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")

def Reset():
    pass

def Clear():
    try:
        if os_name == "Windows":
            os.system("cls")
        else:
            os.system("clear")
    except:
        pass

def CheckWebhook(webhook_url):
    if not webhook_url or not webhook_url.startswith("http"):
        print(f"{BEFORE + AFTER} {ERROR} Invalid webhook URL.{red}")
        return False
    return True

color_webhook = 0x00ff00
username_webhook = "Kernel Tool"
avatar_webhook = ""
