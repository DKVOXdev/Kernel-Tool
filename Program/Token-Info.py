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

        if token_response.status_code == 200:
            token_status = "Valid"
        else:
            token_status = "Invalid"

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

        try:
            account_created = datetime.fromtimestamp(((int(user_api.get('id', 0)) >> 22) + 1420070400000) / 1000, timezone.utc)
        except:
            account_created = "None"

        try:
            premium_type = user_api.get('premium_type', 0)
            if premium_type == 0:
                nitro_status = 'False'
            elif premium_type == 1:
                nitro_status = 'Nitro Classic'
            elif premium_type == 2:
                nitro_status = 'Nitro Boosts'
            elif premium_type == 3:
                nitro_status = 'Nitro Basic'
            else:
                nitro_status = 'False'
        except:
            nitro_status = "None"

        try:
            avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_api.get('avatar')}.gif" if user_api.get('avatar') else "None"
            if avatar_url != "None" and requests.get(avatar_url).status_code != 200:
                avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{user_api.get('avatar')}.png"
        except:
            avatar_url = "None"

        linked_users = "None"
        try:
            linked = user_api.get('linked_users', [])
            if linked:
                linked_users = ' / '.join([f"{u.get('username', '')}#{u.get('discriminator', '')}" for u in linked])
        except:
            pass

        bio = user_api.get('bio', "None") or "None"

        authenticator_types = "None"
        try:
            at = user_api.get('authenticator_types', [])
            if at:
                authenticator_types = ' / '.join(map(str, at))
        except:
            pass

        # Guilds
        total_guilds = "None"
        owned_guild_count = "None"
        owned_guild_names = "None"
        try:
            guilds_api_response = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers={'Authorization': discord_token})
            if guilds_api_response.status_code == 200:
                guilds_data = guilds_api_response.json()
                total_guilds = len(guilds_data)
                owned_guilds = [guild for guild in guilds_data if guild.get('owner')]
                owned_guild_count = f"({len(owned_guilds)})"
                if owned_guilds:
                    owned_guild_names = "\n" + "\n".join([f"{g['name']} ({g['id']})" for g in owned_guilds])
                else:
                    owned_guild_names = "None"
        except:
            pass

        # Billing
        payment_methods = "None"
        try:
            billing_info = requests.get('https://discord.com/api/v6/users/@me/billing/payment-sources', headers={'Authorization': discord_token}).json()
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

        # Friends
        friends = "None"
        try:
            friends_list = requests.get('https://discord.com/api/v8/users/@me/relationships', headers={'Authorization': discord_token}).json()
            if friends_list:
                f_list = []
                for f in friends_list:
                    u = f.get('user', {})
                    f_list.append(f"{u.get('username', '')}#{u.get('discriminator', '')} ({u.get('id', '')})")
                friends = '\n' + ' / '.join(f_list[:20])  # limit to avoid too long
        except:
            pass

        # Gift codes
        gift_codes = "None"
        try:
            gift_codes_list = requests.get('https://discord.com/api/v9/users/@me/outbound-promotions/codes', headers={'Authorization': discord_token}).json()
            if gift_codes_list:
                codes_list = []
                for g in gift_codes_list:
                    promo = g.get('promotion', {}).get('outbound_title', '')
                    code = g.get('code', '')
                    codes_list.append(f"Gift: {promo}\nCode: {code}")
                gift_codes = '\n\n'.join(codes_list)
        except:
            pass

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
 {INFO_ADD} MFA          : {white}{mfa_enabled}{red}
 {INFO_ADD} Authenticator: {white}{authenticator_types}{red}
 {INFO_ADD} Billing      : {white}{payment_methods}{red}
 {INFO_ADD} Gift Codes   : {white}{gift_codes}{red}
 {INFO_ADD} Guilds       : {white}{total_guilds}{red}
 {INFO_ADD} Owner Guilds : {white}{owned_guild_count}{owned_guild_names}{red}
 {INFO_ADD} Bio          : {white}{bio}{red}
 {INFO_ADD} Friends      : {white}{friends}{red}
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
    """)
    Continue()
    Reset()

except Exception as e:
    Error(e)
