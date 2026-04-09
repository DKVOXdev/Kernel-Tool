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

    """Display a title banner."""

    try:

        width = 80

        try:

            import shutil

            width = shutil.get_terminal_size().columns

        except:

            pass

        # Use box drawing characters for better appearance

        box_width = min(width - 4, 70)

        print(f"
╔{'═' * box_width}╗")

        print(f"║{title.center(box_width)}║")

        print(f"╚{'═' * box_width}╝
")

    except:

        print(f"
╔{'═' * 70}╗")

        print(f"║{title.center(70)}║")

        print(f"╚{'═' * 70}╝
")



def Slow(text):

    """Print text slowly."""

    try:

        for char in text:

            print(char, end='', flush=True)

            time.sleep(0.01)

        print()

    except:

        print(text)



def ChoiceUserAgent():

    """Return a random user agent."""

    user_agents = [

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",

        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",

        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"

    ]

    return random.choice(user_agents)



def Choice1TokenDiscord():

    """Get Discord token from user input."""

    token = input(f"{BEFORE + AFTER} {INPUT} Token -> {reset}")

    return token



def Censored(text):

    """Censor sensitive text (placeholder)."""

    pass



def ErrorModule(e):

    """Display error for missing module."""

    print(f"{BEFORE + AFTER} {ERROR} Module Error: {white}{str(e)}{red}")

    print(f"{BEFORE + AFTER} {ERROR} Please install the required module.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def Error(e):

    """Display general error."""

    print(f"{BEFORE + AFTER} {ERROR} Error: {white}{str(e)}{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def ErrorId():

    """Display error for invalid ID."""

    print(f"{BEFORE + AFTER} {ERROR} Invalid ID provided.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def ErrorNumber():

    """Display error for invalid number."""

    print(f"{BEFORE + AFTER} {ERROR} Invalid number provided.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def ErrorChoice():

    """Display error for invalid choice."""

    print(f"{BEFORE + AFTER} {ERROR} Invalid choice.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def ErrorToken():

    """Display error for invalid token."""

    print(f"{BEFORE + AFTER} {ERROR} Invalid token provided.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def OnlyLinux():

    """Display message for Linux-only feature."""

    print(f"{BEFORE + AFTER} {ERROR} This feature is only available on Linux.{red}")

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def Continue():

    """Wait for user to continue."""

    input(f"{BEFORE + AFTER} {INPUT} Press Enter to continue...{reset}")



def Reset():

    """Reset/return to menu (no-op since multitool handles menu)."""

    pass



def Clear():

    """Clear the screen."""

    try:

        if os_name == "Windows":

            os.system("cls")

        else:

            os.system("clear")

    except:

        pass



def CheckWebhook(webhook_url):

    """Check if webhook URL is valid (placeholder)."""

    if not webhook_url or not webhook_url.startswith("http"):

        print(f"{BEFORE + AFTER} {ERROR} Invalid webhook URL.{red}")

        return False

    return True



# Webhook variables (used in some programs)

color_webhook = 0x00ff00

username_webhook = "Kernel Tools"

avatar_webhook = ""
