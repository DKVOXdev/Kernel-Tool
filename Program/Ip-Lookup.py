import requests
import os
import platform

C = "\033[96m"
R = "\033[0m"

if platform.system().lower() == "windows":
    try:
        import ctypes
        ctypes.windll.kernel32.SetConsoleMode(
            ctypes.windll.kernel32.GetStdHandle(-11), 7
        )
    except:
        pass

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def lookup(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,query,country,regionName,city,zip,isp,org,timezone,lat,lon", timeout=10)
        data = r.json()

        if data.get("status") != "success":
            print(f"{C}Erreur API : {data.get('message','N/A')}{R}")
            return

        lat = data.get("lat", "N/A")
        lon = data.get("lon", "N/A")

        print(f"{C}┌──────────────────────────────────────────────┐{R}")
        print(f"{C}│               IP LOOKUP RESULT               │{R}")
        print(f"{C}├──────────────────────────────────────────────┤{R}")
        print(f"{C}│ IP        │ {data.get('query','N/A'):<36} │{R}")
        print(f"{C}│ Pays      │ {data.get('country','N/A'):<36} │{R}")
        print(f"{C}│ Région    │ {data.get('regionName','N/A'):<36} │{R}")
        print(f"{C}│ Ville     │ {data.get('city','N/A'):<36} │{R}")
        print(f"{C}│ Postal    │ {data.get('zip','N/A'):<36} │{R}")
        print(f"{C}│ ISP/Org   │ {data.get('isp','N/A'):<36} │{R}")
        print(f"{C}│ Timezone  │ {data.get('timezone','N/A'):<36} │{R}")
        print(f"{C}│ Latitude  │ {lat:<36} │{R}")
        print(f"{C}│ Longitude │ {lon:<36} │{R}")
        print(f"{C}│ Maps      │ https://maps.google.com/?q={lat},{lon:<9} │{R}")
        print(f"{C}└──────────────────────────────────────────────┘{R}")

    except Exception as e:
        print(f"{C}Erreur connexion ou API : {e}{R}")

def main():
    clear()
    ip = input(f"{C}IP : {R}").strip()
    if ip:
        clear()
        lookup(ip)
        input(f"\n{C}Appuyez sur Entrée pour revenir au menu principal{R}")

if __name__ == "__main__":
    main()