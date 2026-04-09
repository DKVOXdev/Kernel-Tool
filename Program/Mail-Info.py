#!/usr/bin/env python3
# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os
import re
import dns.resolver

C = "\033[96m"
R = "\033[0m"

if os.name == "nt":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except:
        pass

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

resolver = dns.resolver.Resolver(configure=False)
resolver.nameservers = ['8.8.8.8', '8.8.4.4']

def get_email_info(email):
    info = {}
    domain_all = email.split('@')[-1] if '@' in email else "N/A"
    name = email.split('@')[0] if '@' in email else "N/A"
    domain_match = re.search(r"@([^@.]+)\.", email)
    domain = domain_match.group(1) if domain_match else "N/A"
    tld = f".{email.split('.')[-1]}" if '.' in email else "N/A"

    try:
        mx_records = resolver.resolve(domain_all, 'MX')
        info["mx_servers"] = [str(r.exchange) for r in mx_records]
    except:
        info["mx_servers"] = None

    try:
        spf_records = resolver.resolve(domain_all, 'SPF')
        info["spf_records"] = [str(r) for r in spf_records]
    except:
        info["spf_records"] = None

    try:
        dmarc_records = resolver.resolve(f"_dmarc.{domain_all}", 'TXT')
        info["dmarc_records"] = [str(r) for r in dmarc_records]
    except:
        info["dmarc_records"] = None

    info["google_workspace"] = False
    info["microsoft_365"] = False
    if info.get("mx_servers"):
        for server in info["mx_servers"]:
            if "google.com" in server:
                info["google_workspace"] = True
            if "outlook.com" in server:
                info["microsoft_365"] = True

    return info, domain_all, domain, tld, name

def main():
    clear_console()
    email = input(f"{C}Email : {R}").strip()
    if not email:
        print(f"{C}Email invalide{R}")
        return
    clear_console()

    info, domain_all, domain, tld, name = get_email_info(email)

    mx = ", ".join(info.get("mx_servers")) if info.get("mx_servers") else "N/A"
    spf = ", ".join(info.get("spf_records")) if info.get("spf_records") else "N/A"
    dmarc = ", ".join(info.get("dmarc_records")) if info.get("dmarc_records") else "N/A"
    google_ws = str(info.get("google_workspace", False))
    microsoft_365 = str(info.get("microsoft_365", False))

    name = str(name)
    domain = str(domain)
    tld = str(tld)
    domain_all = str(domain_all)

    print(f"{C}┌──────────────────────────────────────────────┐{R}")
    print(f"{C}│               EMAIL LOOKUP RESULT            │{R}")
    print(f"{C}├──────────────────────────────────────────────┤{R}")
    print(f"{C}│ Email         │ {email:<36} │{R}")
    print(f"{C}│ Name          │ {name:<36} │{R}")
    print(f"{C}│ Domain        │ {domain:<36} │{R}")
    print(f"{C}│ TLD           │ {tld:<36} │{R}")
    print(f"{C}│ Domain All    │ {domain_all:<36} │{R}")
    print(f"{C}│ MX Servers    │ {mx:<36} │{R}")
    print(f"{C}│ SPF Records   │ {spf:<36} │{R}")
    print(f"{C}│ DMARC         │ {dmarc:<36} │{R}")
    print(f"{C}│ Google WS     │ {google_ws:<36} │{R}")
    print(f"{C}│ Microsoft 365 │ {microsoft_365:<36} │{R}")
    print(f"{C}└──────────────────────────────────────────────┘{R}")

    input(f"\n{C}Appuyez sur Entrée pour revenir au menu principal{R}")

if __name__ == "__main__":
    main()
