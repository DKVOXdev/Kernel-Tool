# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ------------------------------------------------------------------------------------------------
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner,
#       but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le
#       propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.
# ------------------------------------------------------------------------------------------------

import os
import sys
import time
import random
from datetime import datetime

from .Config import (
    ip_lookup_map_banner,
    email_tracker_banner,
    phone_lookup_banner,
    username_tracker_banner,
    github_lookup_banner,
    fake_identite_banner,
    cookie_login_banner,
    pseudo_info_banner,
    nitro_gen_banner,
    token_info_banner,
    token_login_banner,
    token_server_join_banner,
    token_change_language_banner,
    delete_webhook_banner,
    token_block_friends_banner,
    webhook_spammer_banner,
    iban_generator_banner,
    usb_tool_banner,
    fakevoice_banner,
    exe_to_image_banner,
    create_dox_banner,
    zip_cracker_banner,
    grabber_banner,
    stealer_banner,
)

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

os_name   = "Windows" if os.name == 'nt' else "Linux"
tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INFO        = "[INFO]"
ERROR       = "[ERROR]"
WAIT        = "[WAIT]"
INPUT       = "[INPUT]"
GEN_VALID   = "[VALID]"
GEN_INVALID = "[INVALID]"
ADD         = "[ADD]"
INFO_ADD    = "[+]"
BEFORE      = "[BEFORE]"
AFTER       = "[AFTER]"
SUCCESS     = "[SUCCESS]"
FAILED      = "[FAILED]"
WARNING     = "[WARNING]"
DEBUG       = "[DEBUG]"
FOUND       = "[FOUND]"
NOT_FOUND   = "[NOT FOUND]"
LOAD        = "[LOAD]"
DONE        = "[DONE]"
START       = "[START]"
STOP        = "[STOP]"
SEND        = "[SEND]"
RECV        = "[RECV]"
CHECK       = "[CHECK]"
SKIP        = "[SKIP]"
RETRY       = "[RETRY]"
TIMEOUT     = "[TIMEOUT]"
PROXY       = "[PROXY]"
RESULT      = "[RESULT]"

white = LC
green = LC
red   = LC
blue  = LC
cyan  = LC
reset = RS

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def Title(title):
    pass

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
    token = input(f"\033[96m {INPUT} Token -> \033[0m")
    return token

def Censored(text):
    pass

def ErrorModule(e):
    print(f"\033[96m {ERROR} Module Error: {str(e)}\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def Error(e):
    print(f"\033[96m {ERROR} Error: {str(e)}\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def ErrorId():
    print(f"\033[96m {ERROR} Invalid ID provided.\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def ErrorNumber():
    print(f"\033[96m {ERROR} Invalid number provided.\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def ErrorChoice():
    print(f"\033[96m {ERROR} Invalid choice.\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def ErrorToken():
    print(f"\033[96m {ERROR} Invalid token provided.\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def OnlyLinux():
    print(f"\033[96m {ERROR} This feature is only available on Linux.\033[0m")
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

def Continue():
    input(f"\033[96m {INPUT} Press Enter to continue...\033[0m")

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
        print(f"\033[96m {ERROR} Invalid webhook URL.\033[0m")
        return False
    return True

color_webhook    = 0x00ff00
username_webhook = "Kernel Tool"
avatar_webhook   = ""
