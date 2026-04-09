#!/usr/bin/env python3
# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import requests
import time
from datetime import datetime
import random
import os
import platform

C = "\033[96m"
R = "\033[0m"

INFO = f"{C}[INFO]{R}"
INFO_ADD = f"{C}[+]{R}"
WAIT = f"{C}[WAIT]{R}"
ERROR = f"{C}[ERROR]{R}"
INPUT = f"{C}[INPUT]{R}"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
]

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def current_time_hour():
    return datetime.now().strftime("%H:%M:%S")

def ChoiceUserAgent():
    return random.choice(USER_AGENTS)

def ErrorUsername():
    print(f"[{current_time_hour()}] {ERROR} Invalid username or API error.{R}")
    input(f"{C}Press Enter to try again...{R}")

def Continue():
    input(f"{C}Press Enter to return to menu...{R}")

def get_roblox_info(username_input):
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}
    clear_screen()
    print(f"[{current_time_hour()}] {INFO} Selected User-Agent: {C}{user_agent}{R}")
    print(f"[{current_time_hour()}] {WAIT} Retrieving information...{R}")
    time.sleep(0.8)
    try:
        response = requests.post(
            "https://users.roblox.com/v1/usernames/users",
            headers=headers,
            json={"usernames": [username_input], "excludeBannedUsers": True}
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if not data.get('data') or len(data['data']) == 0:
            return None
        user_id = data['data'][0]['id']
        response = requests.get(f"https://users.roblox.com/v1/users/{user_id}", headers=headers)
        if response.status_code != 200:
            return None
        api = response.json()
        return {
            "userid": api.get('id', "None"),
            "display_name": api.get('displayName', "None"),
            "username": api.get('name', "None"),
            "description": api.get('description', "None"),
            "created_at": api.get('created', "None"),
            "is_banned": api.get('isBanned', "None"),
            "external_app_display_name": api.get('externalAppDisplayName', "None"),
            "has_verified_badge": api.get('hasVerifiedBadge', "None")
        }
    except requests.exceptions.RequestException:
        return None

def main():
    while True:
        clear_screen()
        username_input = input(f"[{current_time_hour()}] {INPUT} Roblox Username -> {R}").strip()
        if not username_input:
            continue
        info = get_roblox_info(username_input)
        if info is None:
            ErrorUsername()
            continue
        clear_screen()
        print(f"""
{C}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Username       : {C}{info['username']}{R}
 {INFO_ADD} Id             : {C}{info['userid']}{R}
 {INFO_ADD} Display Name   : {C}{info['display_name']}{R}
 {INFO_ADD} Description    : {C}{info['description']}{R}
 {INFO_ADD} Created        : {C}{info['created_at']}{R}
 {INFO_ADD} Banned         : {C}{info['is_banned']}{R}
 {INFO_ADD} External Name  : {C}{info['external_app_display_name']}{R}
 {INFO_ADD} Verified Badge : {C}{info['has_verified_badge']}{R}
{C}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
        """)
        Continue()
        break

if __name__ == "__main__":
    main()
