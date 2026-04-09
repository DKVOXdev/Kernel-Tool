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
import json
import time
from datetime import datetime
from faker import Faker
import random
from colorama import Fore, Style, init

init(autoreset=True)

countries = {
    "1": ("France", "fr_FR", "FR", "+33", ["06", "07"]),
    "2": ("Belgium", "fr_BE", "BE", "+32", ["047", "048", "049", "04"]),
    "3": ("Switzerland", "fr_CH", "CH", "+41", ["076", "077", "078", "079"]),
    "4": ("Canada (QC)", "fr_CA", "CA", "+1", ["514", "438", "450", "581", "819", "418", "367"])
}

selected_country = "1"
fake = Faker(countries[selected_country][1])

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def title(text):
    return f"{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}"

def label(text):
    return f"{Fore.MAGENTA}{text:<30}{Style.RESET_ALL}"

def value(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

def header():
    clear_screen()
    print(Fore.RED + "=" * 80)
    print(Fore.RED + r"""
                                          ...:----:...
                                     .:=#@@@@@@@@@@@@@@%*-..
                                  .:#@@@@@@@%#*****#%@@@@@@@+..
                               ..-@@@@@%-...... ........+@@@@@@..
                               :%@@@@=..   .#@@@@@@@@#=....+@@@@*.
                             .+@@@@=.      .*@@@%@@@@@@@@=...*@@@@:.
                            .#@@@%.                 .=@@@@@=. .@@@@-.
                           .=@@@#.                    .:%@@@*. -@@@%:.
                           .%@@@-                       .*@@*. .+@@@=.
                           :@@@#.                              .-@@@#.
                           -@@@#                                :%@@@.
                           :@@@#.                              .-@@@#.
                           .%@@@-.                             .+@@@=.
                           .+@@@#.                             -@@@%:.
                            .*@@@%.                          .:@@@@-.
                             .+@@@@=..                     ..*@@@@:.
                               :%@@@@-..                ...+@@@@*.
                               ..-@@@@@%=...         ...*@@@@@@@@#.
                                  .:*@@@@@@@%*++++**@@@@@@@@=:*@@@@#:.
                                     ..=%@@@@@@@@@@@@@@%#-.   ..*@@@@%:.
                                        .....:::::::....       ...+@@@@%:
                                                                  ..+@@@@%-.
                                                                    ..=@@@@%-.
                                                                      ..=@@@@@=.
                                                                         .=%@@@@=.
                                                                          ..-%@@@-.
                                                                             ....
    """.center(78))
    print(Fore.RED + "=" * 80)
    print()

def generate_mobile():
    _, _, _, phone_prefix, prefixes = countries[selected_country]
    prefix = random.choice(prefixes)
    length = 8 if selected_country in ["1", "2"] else 7
    number = ''.join(str(random.randint(0, 9)) for _ in range(length))
    if selected_country == "1":
        return f"{prefix} {number[:2]} {number[2:4]} {number[4:6]} {number[6:]}"
    elif selected_country == "4":
        return f"{prefix}-{number[:3]}-{number[3:]}"
    else:
        return f"{prefix} {number}"

def phone_int_format(phone_local):
    _, _, _, phone_prefix, _ = countries[selected_country]
    digits = ''.join(filter(str.isdigit, phone_local))
    if digits.startswith("0"):
        digits = digits[1:]
    return f"{phone_prefix}{digits}"

def generate_address():
    country_name, _, country_code, _, _ = countries[selected_country]
    gps_ranges = {
        "FR": (42.3, 51.1, -5.2, 9.6),
        "BE": (49.5, 51.5, 2.5, 6.4),
        "CH": (45.8, 47.8, 5.9, 10.5),
        "CA": (45.0, 50.0, -75.0, -65.0)
    }
    lat_min, lat_max, lon_min, lon_max = gps_ranges.get(country_code, (-90, 90, -180, 180))
    lat = round(random.uniform(lat_min, lat_max), 6)
    lon = round(random.uniform(lon_min, lon_max), 6)
    return {
        "complete": fake.street_address() + ", " + fake.postcode() + " " + fake.city() + ", " + country_name,
        "number": fake.building_number(),
        "street": fake.street_name(),
        "city": fake.city(),
        "postcode": fake.postcode(),
        "country": country_name,
        "country_code": country_code,
        "gps_lat": lat,
        "gps_lon": lon
    }

def generate_birth_date(min_age=18, max_age=80):
    today = datetime.now()
    year = today.year - random.randint(min_age, max_age)
    month = random.randint(1, 12)
    day = random.randint(1, (28 if month == 2 else 30 if month in [4, 6, 9, 11] else 31))
    birth_date = datetime(year, month, day)
    age = today.year - year - ((today.month, today.day) < (month, day))
    return {
        "date": birth_date.strftime("%d/%m/%Y"),
        "age": age,
        "zodiac_sign": get_zodiac_sign(month, day)
    }

def get_zodiac_sign(month, day):
    signs = [
        ((1, 20), "Capricorn"), ((2, 19), "Aquarius"), ((3, 21), "Pisces"),
        ((4, 20), "Aries"), ((5, 21), "Taurus"), ((6, 21), "Gemini"),
        ((7, 23), "Cancer"), ((8, 23), "Leo"), ((9, 23), "Virgo"),
        ((10, 23), "Libra"), ((11, 22), "Scorpio"), ((12, 22), "Sagittarius")
    ]
    for (m, d), sign in signs:
        if month == m and day >= d or month == m % 12 + 1 and day < d:
            return sign
    return "Capricorn"

def generate_ssn(gender, birth_date_str):
    if selected_country != "1":
        return fake.ssn()
    birth_date = datetime.strptime(birth_date_str, "%d/%m/%Y")
    sex = "1" if gender == "M" else "2"
    year = birth_date.strftime("%y")
    month = birth_date.strftime("%m")
    dept = str(random.randint(1, 95)).zfill(2)
    commune = str(random.randint(1, 999)).zfill(3)
    ordre = str(random.randint(1, 999)).zfill(3)
    base = f"{sex}{year}{month}{dept}{commune}{ordre}"
    key = 97 - (int(base) % 97)
    return f"{sex} {year} {month} {dept} {commune} {ordre} {str(key).zfill(2)}"

def create_identity(gender):
    if gender == "random":
        gender = random.choice(["M", "F"])
    firstname = fake.first_name_male() if gender == "M" else fake.first_name_female()
    lastname = fake.last_name()
    birth_info = generate_birth_date()
    phone = generate_mobile()
    ssn = generate_ssn(gender, birth_info["date"])
    address = generate_address()
    email = f"{firstname.lower()}.{lastname.lower()}@{random.choice(['gmail.com', 'outlook.com', 'yahoo.com', 'hotmail.com'])}"
    photo = f"https://randomuser.me/api/portraits/{'men' if gender == 'M' else 'women'}/{random.randint(1, 99)}.jpg"
    identity = {
        "identity": {
            "gender": "Male" if gender == "M" else "Female",
            "first_name": firstname,
            "last_name": lastname,
            "birth_date": birth_info["date"],
            "age": birth_info["age"],
            "zodiac_sign": birth_info["zodiac_sign"],
            "social_security": ssn,
            "email": email,
            "photo": photo
        },
        "address": address,
        "digital": {
            "phone_local": phone,
            "phone_international": phone_int_format(phone),
            "username": fake.user_name(),
            "password": fake.password(length=16, special_chars=True, digits=True, upper_case=True),
            "ipv4_private": fake.ipv4_private(),
            "ipv4_public": fake.ipv4_public(),
            "ipv6": fake.ipv6(),
            "mac": fake.mac_address(),
            "user_agent": fake.user_agent()
        },
        "banking": {
            "card_number": fake.credit_card_number(),
            "card_type": fake.credit_card_provider(),
            "card_expiry": fake.credit_card_expire(),
            "card_cvv": fake.credit_card_security_code(),
            "iban": fake.iban(),
            "bic": fake.swift()
        },
        "company": {
            "name": fake.company(),
            "job": fake.job(),
            "work_email": f"{firstname.lower()}.{lastname.lower()}@{fake.domain_name()}"
        },
        "vehicle": {
            "plate": fake.license_plate(),
            "vin": fake.vin()
        }
    }
    return identity

def export_identity(data):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_name = f"{data['identity']['first_name']}_{data['identity']['last_name']}"
    if not os.path.exists("exports"):
        os.makedirs("exports")
    filename = f"exports/identity_{full_name}_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(Fore.GREEN + f"\nIdentity exported: {filename}")

def show_category(title_txt, data_dict):
    print("\n" + title(f"<< {title_txt} >>") + "\n")
    for k, v in data_dict.items():
        print(f" {label(k)} : {value(v)}")

def display_identity(data):
    clear_screen()
    header()
    show_category("IDENTITY", data["identity"])
    show_category("ADDRESS", data["address"])
    show_category("DIGITAL", data["digital"])
    show_category("BANKING", data["banking"])
    show_category("COMPANY", data["company"])
    show_category("VEHICLE", data["vehicle"])
    print(Fore.YELLOW + "\n[E] Export | [C] Copy | [ENTER] Back")
    choice = input(Fore.GREEN + "\nChoice: ").strip().upper()
    if choice == "E":
        export_identity(data)
    elif choice == "C":
        try:
            import pyperclip
            pyperclip.copy(json.dumps(data, ensure_ascii=False, indent=2))
            print(Fore.GREEN + "\nCopied to clipboard!")
        except ImportError:
            print(Fore.RED + "\npyperclip not installed. Install it via pip.")
    input(Fore.GREEN + "\nPress ENTER...")

def generate_random():
    display_identity(create_identity("random"))

def generate_man():
    display_identity(create_identity("M"))

def generate_woman():
    display_identity(create_identity("F"))

def choose_country():
    global selected_country, fake
    clear_screen()
    header()
    print(title("SELECT COUNTRY:\n"))
    for key, (name, _, _, prefix, _) in countries.items():
        print(f" [{key}] {name} ({prefix})")
    choice = input("\nChoice: ").strip()
    if choice in countries:
        selected_country = choice
        fake = Faker(countries[selected_country][1])
        print(Fore.GREEN + "\nCountry updated!")
    else:
        print(Fore.RED + "\nInvalid choice.")
    input(Fore.GREEN + "\nPress ENTER...")

def create_custom_identity():
    clear_screen()
    header()
    print(Fore.YELLOW + "Enter '0' for automatic generation.")
    gender = input(Fore.RED + "Gender (M/F): ").upper()
    if gender not in ["M", "F"]:
        gender = random.choice(["M", "F"])
    firstname = input(Fore.RED + "First Name: ")
    if firstname == "0":
        firstname = fake.first_name_male() if gender == "M" else fake.first_name_female()
    lastname = input(Fore.RED + "Last Name: ")
    if lastname == "0":
        lastname = fake.last_name()
    email = input(Fore.RED + "Email: ")
    if email == "0":
        email = f"{firstname.lower()}.{lastname.lower()}@{random.choice(['gmail.com', 'outlook.com'])}"
    birth_info = generate_birth_date()
    phone = input(Fore.RED + "Local Phone: ")
    if phone == "0":
        phone = generate_mobile()
    address = generate_address()
    ssn = generate_ssn(gender, birth_info["date"])
    photo = f"https://randomuser.me/api/portraits/{'men' if gender == 'M' else 'women'}/{random.randint(1, 99)}.jpg"
    identity = {
        "identity": {
            "gender": "Male" if gender == "M" else "Female",
            "first_name": firstname,
            "last_name": lastname,
            "birth_date": birth_info["date"],
            "age": birth_info["age"],
            "zodiac_sign": birth_info["zodiac_sign"],
            "social_security": ssn,
            "email": email,
            "photo": photo
        },
        "address": address,
        "digital": {
            "phone_local": phone,
            "phone_international": phone_int_format(phone),
            "username": fake.user_name(),
            "password": fake.password(length=16, special_chars=True, digits=True, upper_case=True),
            "ipv4_private": fake.ipv4_private(),
            "ipv4_public": fake.ipv4_public(),
            "ipv6": fake.ipv6(),
            "mac": fake.mac_address(),
            "user_agent": fake.user_agent()
        },
        "banking": {
            "card_number": fake.credit_card_number(),
            "card_type": fake.credit_card_provider(),
            "card_expiry": fake.credit_card_expire(),
            "card_cvv": fake.credit_card_security_code(),
            "iban": fake.iban(),
            "bic": fake.swift()
        },
        "company": {
            "name": fake.company(),
            "job": fake.job(),
            "work_email": f"{firstname.lower()}.{lastname.lower()}@{fake.domain_name()}"
        },
        "vehicle": {
            "plate": fake.license_plate(),
            "vin": fake.vin()
        }
    }
    display_identity(identity)

def gen_password():
    clear_screen()
    header()
    print(title("PASSWORD GENERATOR\n"))
    try:
        length = int(input(Fore.RED + "Length (8-64): ") or "16")
        length = max(8, min(length, 64))
    except ValueError:
        length = 16
    password = fake.password(length=length, special_chars=True, digits=True, upper_case=True)
    print(Fore.GREEN + f"\nPassword: {password}\n")
    try:
        import pyperclip
        pyperclip.copy(password)
        print(Fore.GREEN + "Copied to clipboard!")
    except ImportError:
        pass
    input(Fore.GREEN + "\nPress ENTER...")

def batch_generate():
    clear_screen()
    header()
    print(title("BATCH GENERATION\n"))
    try:
        count = int(input(Fore.RED + "Number of identities (1-100): "))
        count = max(1, min(count, 100))
        print(Fore.YELLOW + "\n[1] Random  [2] Male  [3] Female")
        type_choice = input(Fore.RED + "\nType: ").strip()
        identities = []
        print(Fore.GREEN + f"\nGenerating {count} identities...")
        for i in range(count):
            gender = "M" if type_choice == "2" else "F" if type_choice == "3" else random.choice(["M", "F"])
            identities.append(create_identity(gender))
            print(Fore.CYAN + f"  {i+1}/{count} generated")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists("exports"):
            os.makedirs("exports")
        filename = f"exports/batch_{count}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(identities, f, ensure_ascii=False, indent=4)
        print(Fore.GREEN + f"\nExported: {filename}")
    except ValueError:
        print(Fore.RED + "\nInvalid number.")
    input(Fore.GREEN + "\nPress ENTER...")

def view_history():
    clear_screen()
    header()
    print(title("EXPORT HISTORY\n"))
    if not os.path.exists("exports"):
        print(Fore.RED + "No exports found.")
        input(Fore.GREEN + "\nPress ENTER...")
        return
    files = sorted(
        [f for f in os.listdir("exports") if f.endswith('.json')],
        key=lambda f: os.path.getmtime(os.path.join("exports", f)),
        reverse=True
    )
    if not files:
        print(Fore.RED + "No exports found.")
    else:
        print(Fore.YELLOW + f"{len(files)} file(s)\n")
        for i, file in enumerate(files, 1):
            path = os.path.join("exports", file)
            size = os.path.getsize(path) // 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y %H:%M")
            print(f"{Fore.CYAN}{i:2}. {Fore.YELLOW}{file} {Fore.GREEN}({size} KB) {Fore.MAGENTA}{mod_time}")
    input(Fore.GREEN + "\nPress ENTER...")

def menu():
    clear_screen()
    header()
    print()
    print(Fore.RED + " [1] Random identity")
    print(Fore.RED + " [2] Male identity")
    print(Fore.RED + " [3] Female identity")
    print(Fore.RED + " [4] Select country")
    print(Fore.RED + " [5] Custom identity")
    print(Fore.RED + " [6] Generate password")
    print(Fore.RED + " [7] Batch identities")
    print(Fore.RED + " [8] View export history")
    print(Fore.RED + " [9] Return to main menu" + Style.RESET_ALL)

def main():
    while True:
        menu()
        choice = input("\nChoice: ").strip()
        if choice == "1":
            generate_random()
        elif choice == "2":
            generate_man()
        elif choice == "3":
            generate_woman()
        elif choice == "4":
            choose_country()
        elif choice == "5":
            create_custom_identity()
        elif choice == "6":
            gen_password()
        elif choice == "7":
            batch_generate()
        elif choice == "8":
            view_history()
        elif choice == "9":
            clear_screen()
            sys.exit(0)
        else:
            input(Fore.RED + "\nInvalid choice. Press ENTER...")

main()
