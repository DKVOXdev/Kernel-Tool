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
import random
from colorama import Fore, Style, init
import sys
import hashlib
from time import sleep
from datetime import datetime, UTC
init(autoreset=True)
iban_formats = {
    'FR': {'length': 27, 'bban': 'BBBBBGSSSCCCCCCCCCCCCCCC', 'name': 'France'},
    'DE': {'length': 22, 'bban': 'BBBBBBBBCCCCCCCCCC', 'name': 'Germany'},
    'ES': {'length': 24, 'bban': 'BBBBGSSSCCCCCCCCCCCC', 'name': 'Spain'},
    'IT': {'length': 27, 'bban': 'KBBBBBBSSSSSCCCCCCCCCCCC', 'name': 'Italy'},
    'GB': {'length': 22, 'bban': 'BBBBSSSSSSCCCCCCCCCC', 'name': 'United Kingdom'},
    'BE': {'length': 16, 'bban': 'BBBCCCCCCCCCC', 'name': 'Belgium'},
    'NL': {'length': 18, 'bban': 'BBBBCCCCCCCCCC', 'name': 'Netherlands'},
    'CH': {'length': 21, 'bban': 'BBBBBKCCCCCCCCCCC', 'name': 'Switzerland'},
    'LU': {'length': 20, 'bban': 'BBBCCCCCCCCCCCCC', 'name': 'Luxembourg'},
    'PT': {'length': 25, 'bban': 'BBBBSSSSCCCCCCCCCCCBB', 'name': 'Portugal'},
    'AT': {'length': 20, 'bban': 'BBBBBCCCCCCCCCCCC', 'name': 'Austria'},
    'IE': {'length': 22, 'bban': 'BBBBSSSSSSCCCCCCCCCC', 'name': 'Ireland'}
}

ascii_banner = Fore.RED + '
 ______  _______    ______   __    __        ________  _______    ______   __    __  _______  
|      \|       \  /      \ |  \  |  \      |        \|       \  /      \ |  \  |  \|       \ 
 \$$$$$$| $$$$$$$\|  $$$$$$\| $$\ | $$      | $$$$$$$$| $$$$$$$\|  $$$$$$\| $$  | $$| $$$$$$$\
  | $$  | $$__/ $$| $$__| $$| $$$\| $$      | $$__    | $$__| $$| $$__| $$| $$  | $$| $$  | $$
  | $$  | $$    $$| $$    $$| $$$$\ $$      | $$  \   | $$    $$| $$    $$| $$  | $$| $$  | $$
  | $$  | $$$$$$$\| $$$$$$$$| $$\$$ $$      | $$$$$   | $$$$$$$\| $$$$$$$$| $$  | $$| $$  | $$
 _| $$_ | $$__/ $$| $$  | $$| $$ \$$$$      | $$      | $$  | $$| $$  | $$| $$__/ $$| $$__/ $$
|   $$ \| $$    $$| $$  | $$| $$  \$$$      | $$      | $$  | $$| $$  | $$ \$$    $$| $$    $$
 \$$$$$$ \$$$$$$$  \$$   \$$ \$$   \$$       \$$       \$$   \$$ \$$   \$$  \$$$$$$  \$$$$$$$ 


FRAUD IBAN GENERATOR by Kernel-Tools v1.1

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
' + Style.RESET_ALL
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def generate_bban(country_code):
    format_str = iban_formats[country_code]['bban']
    return ''.join((str(random.randint(0, 9)) for _ in format_str))
def calculate_check_digits(country_code, bban):
    temp = bban + country_code + '00'
    numeric = ''.join((str(ord(c) - 55) if c.isalpha() else c for c in temp))
    return f'{98 - int(numeric) % 97:02d}'
def generate_iban(country_code):
    bban = generate_bban(country_code)
    check_digits = calculate_check_digits(country_code, bban)
    return f'{country_code}{check_digits}{bban}'
def generate_multiple_ibans(country_code, count=1):
    return [generate_iban(country_code) for _ in range(count)]
def menu():
    clear()
    print(ascii_banner)
    print(Fore.RED + 'Available Countries:
' + Style.RESET_ALL)
    items = list(iban_formats.items())
    col_count = 2
    rows = -(-len(items) // col_count)
    for r in range(rows):
        line_parts = []
        for c in range(col_count):
            i = r + c * rows
            if i < len(items):
                num = f'{i + 1:02}'
                code, data = items[i]
                entry = f"|[{num}] {data['name']:<28}"
                line_parts.append(entry)
        print(Fore.RED + ''.join(line_parts) + Style.RESET_ALL)
    choice = input(Fore.RED + '


→ Country : ' + Style.RESET_ALL).strip('[]')
    if choice == '0':
        print(Fore.RED + '
Closing generator...' + Style.RESET_ALL)
    else:
        try:
            country_code = list(iban_formats.keys())[int(choice) - 1]
        except:
            print(Fore.RED + 'Invalid input.' + Style.RESET_ALL)
            return None
        count = input(Fore.RED + 'How many IBANs to generate? (default=1): ' + Style.RESET_ALL) or '1'
        count = max(1, int(count))
        clear()
        print(ascii_banner)
        print(Fore.RED + f"--- IBANs generated for {iban_formats[country_code]['name']} ---
" + Style.RESET_ALL)
        for iban in generate_multiple_ibans(country_code, count):
            print(Fore.RED + iban + Style.RESET_ALL)
if __name__ == '__main__':
    def clear_screen():
        if os.name == 'posix':
            os.system('clear')
        else:
            os.system('cls')
    clear_screen()
    menu()
    input()
