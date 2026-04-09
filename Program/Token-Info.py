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
    from datetime import datetime, timezone
except Exception as e:
    ErrorModule(e)

Title("Token Info")

try:
    discord_token = Choice1TokenDiscord()
    print(f"{BEFORE + AFTER} {WAIT} Retrieving Information..{reset}")
    try:
        user_api = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': discord_token}).json()

        token_response = requests.get('https://discord.com/api/v8/users/@me', headers={'Authorization': discord_token, 'Content-Type': 'application/json'})

        if token_response.status_code == 200: token_status = "Valid"
        else: token_status = "Invalid"

        username = user_api.get('username', "None") + '#' + user_api.get('discriminator', "None")
        display_name = user_api.get('global_name', "None")
        user_id = user_api.get('id', "None")
        email = user_api.get('email', "None")
        email_verified = user_api.get('verified', "None")
        phone = user_api.get('phone', "None")
        mfa_enabled = user_api.get('mfa_enabled', "None")
        locale = user_api.get('locale', "None")
        avatar = user_api.get('avatar', "None")
        avatar_decoration = user_api.get('avatar_decoration_data', "None")
        public_flags = user_api.get('public_flags', "None")
        flags = user_api.get('flags', "None")
        banner = user_api.get('banner', "None")
        banner_color = user_api.get('banner_color', "None")
        accent_color = user_api.get("accent_color", "None")
        nsfw_allowed = user_api.get('nsfw_allowed', "None")

        try: account_created = datetime.fromtimestamp(((int(user_api.get('id', 'None')) >> 22) + 1420070400000) / 1000, timezone.utc)
        except: account_created = "None"

        try:
            if user_api.get('premium_type', 'None') == 0:
                nitro_status = 'False'
            elif user_api.get('premium_type', 'None') == 1:
                nitro_status = 'Nitro Classic'
            elif user_api.get('premium_type', 'None') == 2:
                nitro_status = 'Nitro Boosts'
            elif user_api.get('premium_type', 'None') == 3:
                nitro_status = 'Nitro Basic'
            else:
                nitro_status = 'False'
        except:
            nitro_status = "None"

        try: avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_api['avatar']}.gif" if requests.get(f"https://cdn.discordapp.com/avatars/{user_id}/{user_api['avatar']}.gif").status_code == 200 else f"https://cdn.discordapp.com/avatars/{user_id}/{user_api['avatar']}.png"
        except: avatar_url = "None"
        
        try:
            linked_users = user_api.get('linked_users', 'None')
            linked_users = ' / '.join(linked_users)
            if not linked_users.strip():
                linked_users = "None"
        except:
            linked_users = "None"
        
        try:
            bio = "
" + user_api.get('bio', 'None')
            if not bio.strip() or bio.isspace():
                bio = "None"
        except:
            bio = "None"
        
        try:
            authenticator_types = user_api.get('authenticator_types', 'None')
            authenticator_types = ' / '.join(authenticator_types)
        except:
            authenticator_types = "None"

        try:
            guilds_api_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': discord_token})
            if guilds_api_response.status_code == 200:
                guilds_data = guilds_api_response.json()
                try:
                    total_guilds = len(guilds_data)
                except:
                    total_guilds = "None"
                try:
                    owned_guilds = [guild for guild in guilds_data if guild['owner']]
                    owned_guild_count = f"({len(owned_guilds)})"
                    owned_guild_names = [] 
                    if owned_guilds:
                        for guild in owned_guilds:
                            owned_guild_names.append(f"{guild['name']} ({guild['id']})")
                        owned_guild_names = "
" + "
".join(owned_guild_names)
                except:
                    owned_guild_count = "None"
                    owned_guild_names = "None" 
        except:
            owned_guild_count = "None"
            total_guilds = "None"
            owned_guild_names = "None"


        try:
            billing_info = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': discord_token}).json()
            if billing_info:
                payment_methods = []

                for payment_method in billing_info:
                    if payment_method['type'] == 1:
                        payment_methods.append('CB')
                    elif payment_method['type'] == 2:
                        payment_methods.append("Paypal")
                    else:
                        payment_methods.append('Other')
                payment_methods = ' / '.join(payment_methods)
            else:
                payment_methods = "None"
        except:
            payment_methods = "None"
        
        try:
            friends_list = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': discord_token}).json()
            if friends_list:
                friends = []
                for friend in friends_list:
                    unprefered_flags = [64, 128, 256, 1048704]
                    friend_data = f"{friend['user']['username']}#{friend['user']['discriminator']} ({friend['user']['id']})"

                    if len('
'.join(friends)) + len(friend_data) >= 1024:
                        break

                    friends.append(friend_data)

                if len(friends) > 0:
                    friends = '
' + ' / '.join(friends)
                else:
                    friends = "None"
            else:
                friends = "None"
        except:
            friends = "None"

        try:
            gift_codes_list = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': discord_token}).json()
            if gift_codes_list:
                codes_list = []
                for gift_code in gift_codes_list:
                    promotion_name = gift_code['promotion']['outbound_title']
                    code_value = gift_code['code']
                    code_data = f"Gift: {promotion_name}
Code: {code_value}"
                    if len('

'.join(codes_list)) + len(code_data) >= 1024:
                        break
                    codes_list.append(code_data)
                if len(codes_list) > 0:
                    gift_codes = '

'.join(codes_list)
                else:
                    gift_codes = "None"
            else:
                gift_codes = "None"
        except:
            gift_codes = "None"

    except Exception as e:
        print(f"{BEFORE + AFTER} {ERROR} Error when retrieving information: {white}{e}")

    Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Status       : {white}{token_status}{red}
 {INFO_ADD} Token        : {white}{discord_token}{red}
 {INFO_ADD} Username     : {white}{username}{red}
 {INFO_ADD} Display Name : {white}{display_name}{red}
 {INFO_ADD} Id           : {white}{user_id}{red}
 {INFO_ADD} Created      : {white}{account_created}{red}
 {INFO_ADD} Country      : {white}{locale}{red}
 {INFO_ADD} Email        : {white}{email}{red}
 {INFO_ADD} Verified     : {white}{email_verified}{red}
 {INFO_ADD} Phone        : {white}{phone}{red}
 {INFO_ADD} Nitro        : {white}{nitro_status}{red}
 {INFO_ADD} Linked Users : {white}{linked_users}{red}
 {INFO_ADD} Avatar Decor : {white}{avatar_decoration}{red}
 {INFO_ADD} Avatar       : {white}{avatar}{red}
 {INFO_ADD} Avatar URL   : {white}{avatar_url}{red}
 {INFO_ADD} Accent Color : {white}{accent_color}{red}
 {INFO_ADD} Banner       : {white}{banner}{red}
 {INFO_ADD} Banner Color : {white}{banner_color}{red}
 {INFO_ADD} Flags        : {white}{flags}{red}
 {INFO_ADD} Public Flags : {white}{public_flags}{red}
 {INFO_ADD} NSFW         : {white}{nsfw_allowed}{red}
 {INFO_ADD} Multi-Factor Authentication : {white}{mfa_enabled}{red}
 {INFO_ADD} Authenticator Type          : {white}{authenticator_types}{red}
 {INFO_ADD} Billing      : {white}{payment_methods}{red}
 {INFO_ADD} Gift Code    : {white}{gift_codes}{red}
 {INFO_ADD} Guilds       : {white}{total_guilds}{red}
 {INFO_ADD} Owner Guilds : {white}{owned_guild_count}{owned_guild_names}{red}
 {INFO_ADD} Bio          : {white}{bio}{red}
 {INFO_ADD} Friend       : {white}{friends}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)
    Continue()
    Reset()
except Exception as e:
    Error(e)
