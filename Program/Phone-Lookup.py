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

import phonenumbers
from phonenumbers import geocoder, carrier, timezone
import os

C = "\033[96m"
R = "\033[0m"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_info(parsed):
    info = {
        "Country": geocoder.description_for_number(parsed, 'en') or "N/A",
        "ISP": carrier.name_for_number(parsed, 'en') or "N/A",
        "Time Zone": ", ".join(timezone.time_zones_for_number(parsed)) or "N/A",
        "National": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
        "International": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
        "E.164": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
    }

    clear_console()
    print(f"{C}┌──────────────────────────────────────────────┐{R}")
    print(f"{C}│           PHONE NUMBER LOOKUP RESULT         │{R}")
    print(f"{C}├──────────────────────────────────────────────┤{R}")
    for k, v in info.items():
        print(f"{C}│ {k:<15} │ {v:<36} │{R}")
    print(f"{C}└──────────────────────────────────────────────┘{R}")

def track(phone_number):
    phone_number = ''.join(filter(str.isdigit, phone_number))

    try:
        parsed = phonenumbers.parse(f"+{phone_number}", None)
        if not phonenumbers.is_valid_number(parsed):
            print(f"{C}[!] Invalid number [!]{R}")
            return False
        show_info(parsed)
        return True
    except:
        print(f"{C}[!] Number error [!]{R}")
        return False

if __name__ == "__main__":
    while True:
        clear_console()
        num = input(f"{C}Number: {R}").strip()

        if not num or num.lower() == "exit":
            break

        ok = track(num)

        if ok:
            next_action = input(f"\n{C}Press Enter to return to menu: {R}").strip()
            if not next_action:
                break
