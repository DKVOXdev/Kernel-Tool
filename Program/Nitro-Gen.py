from Config.Util import *
from Config.Config import *

try:
    import random
    import string
    import json
    import requests
    import threading
except Exception as e:
   ErrorModule(e)

Title("Nitro Gen")

import os
def cls():
    os.system('cls' if os.name == 'nt' else 'clear')

cls()

try:
    use_webhook = input(f"{BEFORE + AFTER} {INPUT} Webhook ? (y/n) -> {reset}")
    if use_webhook in ['y', 'Y', 'Yes', 'yes', 'YES']:
        webhook_url = input(f"{BEFORE + AFTER} {INPUT} Webhook Url -> {reset}")
        CheckWebhook(webhook_url)

    try:
        thread_count = int(input(f"{BEFORE + AFTER} {INPUT} Threads Number -> {reset}"))
    except:
        ErrorNumber()

    def send_webhook(nitro_url):
        webhook_payload = {
        'embeds': [{
                    'title': f'Nitro Valid !',
                    'description': f"**Nitro:**\n```{nitro_url}```",
                    'color': color_webhook,
                    'footer': {
                    "text": username_webhook,
                    "icon_url": avatar_webhook,
                    }
                }],
        'username': username_webhook,
        'avatar_url': avatar_webhook
        }

        webhook_headers = {
        'Content-Type': 'application/json'
        }

        requests.post(webhook_url, data=json.dumps(webhook_payload), headers=webhook_headers)

    def check_nitro():
        nitro_code = ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(16)])
        nitro_url = f'https://discord.gift/{nitro_code}'
        api_response = requests.get(f'https://discordapp.com/api/v6/entitlements/gift-codes/{nitro_code}?with_application=false&with_subscription_plan=true', timeout=1)
        if api_response.status_code == 200:
            if use_webhook in ['y']:
                send_webhook(nitro_url)
            print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Status:  {white}Valid{green}  Nitro: {white}{nitro_url}{reset}")
        else:
            print(f"{BEFORE + AFTER} {GEN_INVALID} Status: {white}Invalid{red} Nitro: {white}{nitro_url}{reset}")

    def run_threads():
        thread_list = []
        try:
            for _ in range(int(thread_count)):
                thread = threading.Thread(target=check_nitro)
                thread.start()
                thread_list.append(thread)
        except:
            ErrorNumber()

        for thread in thread_list:
            thread.join()

    while True:
        run_threads()

except Exception as e:
    Error(e)