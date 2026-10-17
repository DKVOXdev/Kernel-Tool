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

import phonenumbers
from phonenumbers import geocoder, carrier, timezone

from Config.Util import *
from Config.Config import *

os.system('cls' if os.name == 'nt' else 'clear')
Title("Phone Lookup")
print(phone_lookup_banner)

try:
    phone_number = input(f"{LC}{current_time_hour()} {INPUT} Phone Number -> {RS}")

    try:
        parsed_number = phonenumbers.parse(phone_number, None)

        if phonenumbers.is_valid_number(parsed_number):
            status = "Valid"
        else:
            status = "Invalid"

        country_code = f"+{parsed_number.country_code}" if parsed_number.country_code else "None"

        try: operator = carrier.name_for_number(parsed_number, "fr") or "None"
        except: operator = "None"

        try:
            number_type = phonenumbers.number_type(parsed_number)
            type_number = "Mobile" if number_type == phonenumbers.PhoneNumberType.MOBILE else "Fixe"
        except: type_number = "None"

        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else "None"
        except: timezone_info = "None"

        try: country = phonenumbers.region_code_for_number(parsed_number) or "None"
        except: country = "None"

        try: region = geocoder.description_for_number(parsed_number, "fr") or "None"
        except: region = "None"

        try: formatted_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL) or "None"
        except: formatted_number = "None"

        print(f"""
{LC}────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Phone        : {phone_number}
 {INFO_ADD} Formatted    : {formatted_number}
 {INFO_ADD} Status       : {status}
 {INFO_ADD} Country Code : {country_code}
 {INFO_ADD} Country      : {country}
 {INFO_ADD} Region       : {region}
 {INFO_ADD} Timezone     : {timezone_info}
 {INFO_ADD} Operator     : {operator}
 {INFO_ADD} Type Number  : {type_number}
{LC}────────────────────────────────────────────────────────────────────────────────────
{RS}""")

        Continue()
        Reset()

    except:
        print(f"\n{LC} {INFO} Invalid Format !{RS}")
        Continue()
        Reset()

except Exception as e:
    Error(e)
