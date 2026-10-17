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
import datetime

from Config.Util import *
from Config.Config import *

try:
    import requests
except Exception as e:
    ErrorModule(e)

os.system('cls' if os.name == 'nt' else 'clear')
Title("Ip Lookup")
print(ip_lookup_map_banner)

try:
    ip = input(f"\n\033[96m{current_time_hour()} {INPUT} Ip -> \033[0m")

    response = requests.get(f"http://ip-api.com/json/{ip}")
    api = response.json()

    status       = "Valid" if api.get('status') == "success" else "Invalid"
    country      = api.get('country', "None")
    country_code = api.get('countryCode', "None")
    region       = api.get('regionName', "None")
    region_code  = api.get('region', "None")
    zip_code     = api.get('zip', "None")
    city         = api.get('city', "None")
    latitude     = api.get('lat', "None")
    longitude    = api.get('lon', "None")
    timezone     = api.get('timezone', "None")
    isp          = api.get('isp', "None")
    org          = api.get('org', "None")
    as_host      = api.get('as', "None")

    print(f"""
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Status    : {status}
 {INFO_ADD} Country   : {country} ({country_code})
 {INFO_ADD} Region    : {region} ({region_code})
 {INFO_ADD} Zip       : {zip_code}
 {INFO_ADD} City      : {city}
 {INFO_ADD} Latitude  : {latitude}
 {INFO_ADD} Longitude : {longitude}
 {INFO_ADD} Timezone  : {timezone}
 {INFO_ADD} Isp       : {isp}
 {INFO_ADD} Org       : {org}
 {INFO_ADD} As        : {as_host}
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m""")

    Continue()
    Reset()
except Exception as e:
    Error(e)
    input("\n\033[96mPress Enter to exit...\033[0m")
