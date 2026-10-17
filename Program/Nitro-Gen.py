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

from Config.Util import *
from Config.Config import *

try:
    import random
    import string
    import json
    import requests
    import threading
    import os
except Exception as e:
    ErrorModule(e)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

Title("Nitro Gen")
clear()
print(nitro_gen_banner)

try:
    use_webhook = input(f"{LC}{BEFORE + AFTER} {INPUT} Webhook ? (y/n) -> {RS}").strip()

    webhook_url = None
    if use_webhook.lower() in ['y', 'yes']:
        webhook_url = input(f"{LC}{BEFORE + AFTER} {INPUT} Webhook Url -> {RS}").strip()
        if not CheckWebhook(webhook_url):
            webhook_url = None

    try:
        thread_count = int(input(f"{LC}{BEFORE + AFTER} {INPUT} Threads Number -> {RS}"))
    except:
        ErrorNumber()
        thread_count = 1

    clear()
    print(nitro_gen_banner)

    def send_webhook(nitro_url):
        if not webhook_url:
            return
        webhook_payload = {
            'embeds': [{
                'title': 'Nitro Valid !',
                'description': f"**Nitro Verified:**\n```{nitro_url}```",
                'color': color_webhook,
                'footer': {
                    "text": username_webhook,
                    "icon_url": avatar_webhook,
                }
            }],
            'username': username_webhook,
            'avatar_url': avatar_webhook
        }
        webhook_headers = {'Content-Type': 'application/json'}
        try:
            requests.post(webhook_url, data=json.dumps(webhook_payload), headers=webhook_headers)
        except:
            pass

    def check_nitro():
        nitro_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
        nitro_url  = f'https://discord.gift/{nitro_code}'
        try:
            api_response = requests.get(
                f'https://discordapp.com/api/v6/entitlements/gift-codes/{nitro_code}?with_application=false&with_subscription_plan=true',
                timeout=1
            )
        except:
            api_response = type('obj', (object,), {'status_code': 404})()

        if api_response.status_code == 200:
            send_webhook(nitro_url)
            print(f"{LC}{BEFORE + AFTER} {GEN_VALID} Status: Valid | Nitro: {nitro_url}{RS}")
        else:
            print(f"{LC}{BEFORE + AFTER} {GEN_INVALID} Status: Invalid | Nitro: {nitro_url}{RS}")

    def run_threads():
        thread_list = []
        for _ in range(thread_count):
            t = threading.Thread(target=check_nitro)
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join()

    print(f"{LC}Nitro Generator started with {thread_count} threads...{RS}\n")

    while True:
        run_threads()

except Exception as e:
    Error(e)
