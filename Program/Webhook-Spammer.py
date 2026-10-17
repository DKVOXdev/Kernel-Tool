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
    import requests
    import json
    import threading
except Exception as e:
    ErrorModule(e)

Reset()
print(webhook_spammer_banner)
Title("Webhook Spammer")

NUKE_MESSAGE = "# @everyone nuked by Kernel https://guns.lol/2437"
KERNEL_LOGO_URL = None

def main():
    try:
        print(f"{LC}{current_time_hour()} {INFO} This tool will spam a Discord webhook with a fixed message.{RS}")

        webhook_url = input(f"{LC}{current_time_hour()} {INPUT} Webhook URL -> {RS}").strip()

        if not webhook_url:
            print(f"{LC}{current_time_hour()} {ERROR} No webhook URL provided.{RS}")
            Continue()
            Reset()
            return

        if not CheckWebhook(webhook_url):
            print(f"{LC}{current_time_hour()} {ERROR} Invalid webhook URL format.{RS}")
            Continue()
            Reset()
            return

        try:
            threads_number = int(input(f"{LC}{current_time_hour()} {INPUT} Threads Number -> {RS}"))
            if threads_number < 1:
                threads_number = 1
        except:
            ErrorNumber()
            Reset()
            return

        def send_webhook(webhook_url_to_use):
            headers = {'Content-Type': 'application/json'}
            payload = {
                'content': NUKE_MESSAGE,
                'username': 'KERNEL'
            }
            if KERNEL_LOGO_URL and isinstance(KERNEL_LOGO_URL, str) and KERNEL_LOGO_URL.startswith('http'):
                payload['avatar_url'] = KERNEL_LOGO_URL

            try:
                response = requests.post(webhook_url_to_use, headers=headers, data=json.dumps(payload))
                if response.status_code == 204:
                    print(f"{LC}{current_time_hour()} {GEN_VALID} Message sent successfully{RS}")
                elif response.status_code == 429:
                    print(f"{LC}{current_time_hour()} {GEN_INVALID} Rate Limited{RS}")
                else:
                    print(f"{LC}{current_time_hour()} {GEN_INVALID} Status: {response.status_code}{RS}")
            except Exception as e:
                print(f"{LC}{current_time_hour()} {GEN_INVALID} Error: {str(e)[:50]}{RS}")

        def spam_webhook():
            while True:
                send_webhook(webhook_url)

        print(f"{LC}{current_time_hour()} {WAIT} Starting spam with {threads_number} threads...{RS}")
        print(f"{LC}{current_time_hour()} {INFO} Message: {NUKE_MESSAGE}{RS}")

        def run_threads():
            threads = []
            for _ in range(threads_number):
                t = threading.Thread(target=spam_webhook, daemon=True)
                t.start()
                threads.append(t)
            for thread in threads:
                thread.join()

        try:
            run_threads()
        except KeyboardInterrupt:
            print(f"{LC}{current_time_hour()} {INFO} Stopping spam...{RS}")
            Continue()
            Reset()
        except Exception as e:
            Error(e)

    except Exception as e:
        Error(e)

main()
