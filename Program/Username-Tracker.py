#!/usr/bin/env python3
import requests
import os
import threading
import itertools
import time

BLUE = "\033[96m"
RESET = "\033[0m"

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(stop_event):
    spinner = itertools.cycle(["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"])
    while not stop_event.is_set():
        print(f"\r{BLUE}Recherche en cours {next(spinner)}{RESET}", end="", flush=True)
        time.sleep(0.1)
    print("\r" + " " * 30 + "\r", end="")

def username_tracker(username):
    sites = {
        "GitHub": f"https://github.com/{username}",
        "GitLab": f"https://gitlab.com/{username}",
        "Twitter": f"https://twitter.com/{username}",
        "Instagram": f"https://www.instagram.com/{username}/",
        "Reddit": f"https://www.reddit.com/user/{username}",
        "TikTok": f"https://www.tiktok.com/@{username}",
        "Twitch": f"https://www.twitch.tv/{username}",
        "SoundCloud": f"https://soundcloud.com/{username}",
        "Steam": f"https://steamcommunity.com/id/{username}",
        "Medium": f"https://medium.com/@{username}"
    }

    stop_event = threading.Event()
    t = threading.Thread(target=loading_animation, args=(stop_event,))
    t.start()

    results = []

    for site, url in sites.items():
        try:
            r = requests.get(url, timeout=5)
            found = r.status_code == 200
        except:
            found = False
        results.append((site, url, found))

    stop_event.set()
    t.join()

    print(f"{BLUE}Résultats pour '{username}':\n{RESET}")
    for site, url, found in results:
        status = "[+]" if found else "[-]"
        print(f"{BLUE}{status} {site}: {url}{RESET}")

if __name__ == "__main__":
    while True:
        clear_console()
        user = input(f"{BLUE}👤 Pseudo: {RESET}").strip()
        if not user:
            print(f"{BLUE}Au revoir !{RESET}")
            break

        clear_console()
        username_tracker(user)

        again = input(f"\n{BLUE}Entrée revenir au menu: {RESET}").strip()
        if not again:
            print(f"{BLUE}Au revoir !{RESET}")
            break
