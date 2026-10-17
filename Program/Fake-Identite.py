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
import datetime as _dt
from faker import Faker
import random
from colorama import Fore, Style, init
from Config.Config import *
from Config.Util import *

datetime = _dt.datetime

init(autoreset=True)

countries = {
    "1": ("France", "fr_FR", "FR", "+33", ["06", "07"]),
    "2": ("Belgium", "fr_BE", "BE", "+32", ["047", "048", "049", "04"]),
    "3": ("Switzerland", "fr_CH", "CH", "+41", ["076", "077", "078", "079"]),
    "4": ("Canada (QC)", "fr_CA", "CA", "+1", ["514", "438", "450", "581", "819", "418", "367"])
}

selected_country = "1"
fake = Faker(countries[selected_country][1])

def header():
    Clear()
    print(fake_identite_banner)

def label(text):
    return f"\033[96m{text:<30}\033[0m"

def value(text):
    return f"\033[96m{text}\033[0m"

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
    print(f"\033[96m\n {INFO_ADD} Identity exported: {filename}\033[0m")

def show_category(title_txt, data_dict):
    print(f"\n\033[96m<< {title_txt} >>\033[0m\n")
    for k, v in data_dict.items():
        print(f" {label(k)} : {value(str(v))}")

def display_identity(data):
    header()
    show_category("IDENTITY", data["identity"])
    show_category("ADDRESS", data["address"])
    show_category("DIGITAL", data["digital"])
    show_category("BANKING", data["banking"])
    show_category("COMPANY", data["company"])
    show_category("VEHICLE", data["vehicle"])
    print(f"\033[96m\n [E] Export | [C] Copy | [ENTER] Back\033[0m")
    choice = input(f"\033[96m\n {INPUT} Choice: \033[0m").strip().upper()
    if choice == "E":
        export_identity(data)
        Continue()
    elif choice == "C":
        try:
            import pyperclip
            pyperclip.copy(json.dumps(data, ensure_ascii=False, indent=2))
            print(f"\033[96m\n {INFO_ADD} Copied to clipboard!\033[0m")
        except ImportError:
            print(f"\033[96m {ERROR} pyperclip not installed.\033[0m")
        Continue()

def generate_random():
    display_identity(create_identity("random"))

def generate_man():
    display_identity(create_identity("M"))

def generate_woman():
    display_identity(create_identity("F"))

def choose_country():
    global selected_country, fake
    header()
    print(f"\033[96m SELECT COUNTRY:\n\033[0m")
    for key, (name, _, _, prefix, _) in countries.items():
        print(f"\033[96m [{key}] {name} ({prefix})\033[0m")
    choice = input(f"\033[96m\n {INPUT} Choice: \033[0m").strip()
    if choice in countries:
        selected_country = choice
        fake = Faker(countries[selected_country][1])
        print(f"\033[96m\n {INFO_ADD} Country updated!\033[0m")
    else:
        print(f"\033[96m {ERROR} Invalid choice.\033[0m")
    Continue()

def create_custom_identity():
    header()
    print(f"\033[96m Enter '0' for automatic generation.\033[0m")
    gender = input(f"\033[96m {INPUT} Gender (M/F): \033[0m").upper()
    if gender not in ["M", "F"]:
        gender = random.choice(["M", "F"])
    firstname = input(f"\033[96m {INPUT} First Name: \033[0m")
    if firstname == "0":
        firstname = fake.first_name_male() if gender == "M" else fake.first_name_female()
    lastname = input(f"\033[96m {INPUT} Last Name: \033[0m")
    if lastname == "0":
        lastname = fake.last_name()
    email = input(f"\033[96m {INPUT} Email: \033[0m")
    if email == "0":
        email = f"{firstname.lower()}.{lastname.lower()}@{random.choice(['gmail.com', 'outlook.com'])}"
    birth_info = generate_birth_date()
    phone = input(f"\033[96m {INPUT} Local Phone: \033[0m")
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
    header()
    print(f"\033[96m PASSWORD GENERATOR\n\033[0m")
    try:
        length = int(input(f"\033[96m {INPUT} Length (8-64): \033[0m") or "16")
        length = max(8, min(length, 64))
    except ValueError:
        length = 16
    password = fake.password(length=length, special_chars=True, digits=True, upper_case=True)
    print(f"\033[96m\n {INFO_ADD} Password: {password}\n\033[0m")
    try:
        import pyperclip
        pyperclip.copy(password)
        print(f"\033[96m {INFO_ADD} Copied to clipboard!\033[0m")
    except ImportError:
        pass
    Continue()

def batch_generate():
    header()
    print(f"\033[96m BATCH GENERATION\n\033[0m")
    try:
        count = int(input(f"\033[96m {INPUT} Number of identities (1-100): \033[0m"))
        count = max(1, min(count, 100))
        print(f"\033[96m\n [1] Random  [2] Male  [3] Female\033[0m")
        type_choice = input(f"\033[96m {INPUT} Type: \033[0m").strip()
        identities = []
        print(f"\033[96m\n Generating {count} identities...\033[0m")
        for i in range(count):
            gender = "M" if type_choice == "2" else "F" if type_choice == "3" else random.choice(["M", "F"])
            identities.append(create_identity(gender))
            print(f"\033[96m  {i+1}/{count} generated\033[0m")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not os.path.exists("exports"):
            os.makedirs("exports")
        filename = f"exports/batch_{count}_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(identities, f, ensure_ascii=False, indent=4)
        print(f"\033[96m\n {INFO_ADD} Exported: {filename}\033[0m")
    except ValueError:
        print(f"\033[96m {ERROR} Invalid number.\033[0m")
    Continue()

def view_history():
    header()
    print(f"\033[96m EXPORT HISTORY\n\033[0m")
    if not os.path.exists("exports"):
        print(f"\033[96m {ERROR} No exports found.\033[0m")
        Continue()
        return
    files = sorted(
        [f for f in os.listdir("exports") if f.endswith('.json')],
        key=lambda f: os.path.getmtime(os.path.join("exports", f)),
        reverse=True
    )
    if not files:
        print(f"\033[96m {ERROR} No exports found.\033[0m")
    else:
        print(f"\033[96m {len(files)} file(s)\n\033[0m")
        for i, file in enumerate(files, 1):
            path = os.path.join("exports", file)
            size = os.path.getsize(path) // 1024
            mod_time = datetime.fromtimestamp(os.path.getmtime(path)).strftime("%d/%m/%Y %H:%M")
            print(f"\033[96m  {i:2}. {file} ({size} KB) {mod_time}\033[0m")
    Continue()

def menu():
    header()
    print()
    print(f"\033[96m [1] Random identity\033[0m")
    print(f"\033[96m [2] Male identity\033[0m")
    print(f"\033[96m [3] Female identity\033[0m")
    print(f"\033[96m [4] Select country\033[0m")
    print(f"\033[96m [5] Custom identity\033[0m")
    print(f"\033[96m [6] Generate password\033[0m")
    print(f"\033[96m [7] Batch identities\033[0m")
    print(f"\033[96m [8] View export history\033[0m")
    print(f"\033[96m [9] Return to main menu\033[0m")

try:
    def main():
        while True:
            menu()
            choice = input(f"\033[96m\n {INPUT} Choice: \033[0m").strip()
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
                print(f"\033[96m\n {INFO_ADD} Goodbye!\033[0m")
                sys.exit(0)
            else:
                Error("Invalid choice.")

    main()
except Exception as e:
    Error(e)
