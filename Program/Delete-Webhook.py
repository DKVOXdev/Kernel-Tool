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
except Exception as e:
    ErrorModule(e)

Title("Delete Webhook")

try:
    Reset()
    print(delete_webhook_banner)

    print(f"{LC}{BEFORE + AFTER} {INFO} This tool will permanently delete a Discord webhook.{RS}")
    print(f"{LC}{BEFORE + AFTER} {WAIT} Make sure you have the correct webhook URL.{RS}\n")

    webhook_url = input(f"{LC}{BEFORE + AFTER} {INPUT} Webhook URL -> {RS}").strip()

    if not webhook_url:
        print(f"{LC}{BEFORE + AFTER} {ERROR} No webhook URL provided.{RS}")
        Continue()
        Reset()

    if not CheckWebhook(webhook_url):
        print(f"{LC}{BEFORE + AFTER} {ERROR} Invalid webhook URL format.{RS}")
        print(f"{LC}{BEFORE + AFTER} {INFO} Webhook URLs should start with 'https://discord.com/api/webhooks/' or 'https://discordapp.com/api/webhooks/'.{RS}")
        Continue()
        Reset()

    print(f"\n{LC}{BEFORE + AFTER} {WAIT} Attempting to delete webhook...{RS}")

    try:
        response = requests.delete(webhook_url)

        if response.status_code == 204:
            print(f"{LC}{BEFORE + AFTER} {GEN_VALID} Webhook Successfully Deleted!{RS}")
            print(f"{LC}{BEFORE + AFTER} {INFO} Status Code: {response.status_code}{RS}")
        elif response.status_code == 404:
            print(f"{LC}{BEFORE + AFTER} {ERROR} Webhook Not Found.{RS}")
            print(f"{LC}{BEFORE + AFTER} {INFO} The webhook may have already been deleted or the URL is incorrect.{RS}")
        else:
            print(f"{LC}{BEFORE + AFTER} {ERROR} Failed to delete webhook.{RS}")
            print(f"{LC}{BEFORE + AFTER} {INFO} Status Code: {response.status_code}{RS}")
            print(f"{LC}{BEFORE + AFTER} {INFO} Response: {response.text[:100]}{RS}")

    except requests.exceptions.RequestException as e:
        print(f"{LC}{BEFORE + AFTER} {ERROR} Connection Error: {str(e)[:100]}{RS}")
    except Exception as e:
        print(f"{LC}{BEFORE + AFTER} {ERROR} Unexpected Error: {str(e)[:100]}{RS}")

    Continue()
    Reset()

except Exception as e:
    Error(e)
