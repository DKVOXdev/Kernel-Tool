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

import random
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.Util import *

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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_bban(country_code):
    format_str = iban_formats[country_code]['bban']
    return ''.join(str(random.randint(0, 9)) for _ in format_str)

def calculate_check_digits(country_code, bban):
    temp = bban + country_code + '00'
    numeric = ''.join(str(ord(c) - 55) if c.isalpha() else c for c in temp)
    return f'{98 - int(numeric) % 97:02d}'

def generate_iban(country_code):
    bban = generate_bban(country_code)
    check_digits = calculate_check_digits(country_code, bban)
    return f'{country_code}{check_digits}{bban}'

def generate_multiple_ibans(country_code, count=1):
    return [generate_iban(country_code) for _ in range(count)]

def main():
    clear()
    print(iban_generator_banner)
    Title("IBAN Generator")

    print(f"{LC}{current_time_hour()} {INFO} Available Countries:{RS}\n")

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
                entry = f"[{num}] {data['name']:<28}"
                line_parts.append(entry)
        print(f"{LC}  {'  '.join(line_parts)}{RS}")

    choice = input(f"\n{LC}{current_time_hour()} {INPUT} Country: {RS}").strip()

    if choice == '0':
        print(f"{LC}{current_time_hour()} {INFO} Closing generator...{RS}")
        Continue()
        clear()
        return

    try:
        country_code = list(iban_formats.keys())[int(choice) - 1]
    except:
        print(f"{LC}{current_time_hour()} {ERROR} Invalid input.{RS}")
        Continue()
        clear()
        return

    count_input = input(f"{LC}{current_time_hour()} {INPUT} How many IBANs? (default=1): {RS}").strip()
    count = max(1, int(count_input) if count_input.isdigit() else 1)

    clear()
    print(iban_generator_banner)
    print(f"{LC}{current_time_hour()} {INFO} IBANs generated for {iban_formats[country_code]['name']}:{RS}\n")

    for iban in generate_multiple_ibans(country_code, count):
        print(f"{LC}  {iban}{RS}")

    Continue()
    clear()

if __name__ == '__main__':
    main()
