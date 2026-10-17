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

import requests
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'Config'))

from Config.Config import *
from Config.Util import *

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

def ErrorUsername():
    print(f"{LC}[{current_time_hour()}] [ERROR] Invalid username or API error.{RS}")
    input(f"{LC}[INPUT] Press Enter to try again...{RS}")

def get_roblox_info(username_input):
    user_agent = ChoiceUserAgent()
    headers = {"User-Agent": user_agent}

    print(f"{LC}[{current_time_hour()}] [INFO] Selected User-Agent: {user_agent}{RS}")
    print(f"{LC}[{current_time_hour()}] [WAIT] Retrieving information...{RS}")
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
            "userid":                    api.get('id',                      "None"),
            "display_name":              api.get('displayName',             "None"),
            "username":                  api.get('name',                    "None"),
            "description":               api.get('description',             "None"),
            "created_at":                api.get('created',                 "None"),
            "is_banned":                 api.get('isBanned',                "None"),
            "external_app_display_name": api.get('externalAppDisplayName',  "None"),
            "has_verified_badge":        api.get('hasVerifiedBadge',        "None")
        }
    except requests.exceptions.RequestException:
        return None

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(pseudo_info_banner)

    while True:
        username_input = input(f"{LC}[{current_time_hour()}] [INPUT] Roblox Username -> {RS}").strip()
        if not username_input:
            continue

        info = get_roblox_info(username_input)
        if info is None:
            ErrorUsername()
            continue

        sep = f"{LC}{'─' * 100}{RS}"
        print(f"\n{sep}")
        print(f" {LC}[+]{RS} Username       : {LC}{info['username']}{RS}")
        print(f" {LC}[+]{RS} Id             : {LC}{info['userid']}{RS}")
        print(f" {LC}[+]{RS} Display Name   : {LC}{info['display_name']}{RS}")
        print(f" {LC}[+]{RS} Description    : {LC}{info['description']}{RS}")
        print(f" {LC}[+]{RS} Created        : {LC}{info['created_at']}{RS}")
        print(f" {LC}[+]{RS} Banned         : {LC}{info['is_banned']}{RS}")
        print(f" {LC}[+]{RS} External Name  : {LC}{info['external_app_display_name']}{RS}")
        print(f" {LC}[+]{RS} Verified Badge : {LC}{info['has_verified_badge']}{RS}")
        print(f"{sep}\n")

        input(f"{LC}[INPUT] Press Enter to continue...{RS}")
        break

if __name__ == "__main__":
    main()
