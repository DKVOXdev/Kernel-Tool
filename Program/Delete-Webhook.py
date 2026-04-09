# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

from Config.Util import *

from Config.Config import *



try:

    import requests

except Exception as e:

    ErrorModule(e)



Title("Delete Webhook")



try:

    print(f"{BEFORE + AFTER} {INFO} This tool will permanently delete a Discord webhook.{green}")

    print(f"{BEFORE + AFTER} {WAIT} Make sure you have the correct webhook URL.{green}\n")

    

    webhook_url = input(f"{BEFORE + AFTER} {INPUT} Webhook URL -> {reset}").strip()

    

    if not webhook_url:

        print(f"{BEFORE + AFTER} {ERROR} No webhook URL provided.{red}")

        Continue()

        Reset()

    

    # Validate webhook URL

    if not CheckWebhook(webhook_url):

        print(f"{BEFORE + AFTER} {ERROR} Invalid webhook URL format.{red}")

        print(f"{BEFORE + AFTER} {INFO} Webhook URLs should start with 'https://discord.com/api/webhooks/' or 'https://discordapp.com/api/webhooks/'.{green}")

        Continue()

        Reset()

    

    # Confirm deletion

    print(f"\n{BEFORE + AFTER} {WAIT} Attempting to delete webhook...{green}")

    

    try:

        response = requests.delete(webhook_url)

        

        if response.status_code == 204:

            print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Webhook Successfully Deleted!{green}")

            print(f"{BEFORE_GREEN + AFTER_GREEN} {INFO} Status Code: {white}{response.status_code}{green}")

        elif response.status_code == 404:

            print(f"{BEFORE + AFTER} {ERROR} Webhook Not Found.{red}")

            print(f"{BEFORE + AFTER} {INFO} The webhook may have already been deleted or the URL is incorrect.{green}")

        else:

            print(f"{BEFORE + AFTER} {ERROR} Failed to delete webhook.{red}")

            print(f"{BEFORE + AFTER} {INFO} Status Code: {white}{response.status_code}{red}")

            print(f"{BEFORE + AFTER} {INFO} Response: {white}{response.text[:100]}{red}")

            

    except requests.exceptions.RequestException as e:

        print(f"{BEFORE + AFTER} {ERROR} Connection Error: {white}{str(e)[:100]}{red}")

    except Exception as e:

        print(f"{BEFORE + AFTER} {ERROR} Unexpected Error: {white}{str(e)[:100]}{red}")

    

    Continue()

    Reset()



except Exception as e:

    Error(e)


