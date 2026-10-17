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

Reset()
print(token_server_join_banner)
Title("Token Server Join")

try:
    def join_server(discord_token, invite_link):
        invite_code = invite_link.split("/")[-1]

        try:
            invite_response = requests.get(f"https://discord.com/api/v9/invites/{invite_code}")
            if invite_response.status_code == 200:
                server_name = invite_response.json().get('guild', {}).get('name')
            else:
                server_name = invite_link
        except:
            server_name = invite_link

        try:
            join_response = requests.post(
                f"https://discord.com/api/v9/invites/{invite_code}",
                headers={'Authorization': discord_token}
            )
            if join_response.status_code == 200:
                print(f"{LC}{current_time_hour()} {GEN_VALID} Joined: {server_name}{RS}")
            else:
                print(f"{LC}{current_time_hour()} {ERROR} Error {join_response.status_code} | Server: {server_name}{RS}")
        except:
            print(f"{LC}{current_time_hour()} {ERROR} Error | Server: {server_name}{RS}")

    discord_token = Choice1TokenDiscord()
    invite_link = input(f"{LC}{current_time_hour()} {INPUT} Server Invitation -> {RS}")
    join_server(discord_token, invite_link)
    Continue()
    Reset()

except Exception as e:
    Error(e)
