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

import instaloader
import sys
import os
import threading
import itertools
import time
from contextlib import contextmanager

BLUE = "\033[96m"
RESET = "\033[0m"

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def loading_animation(stop_event):
    spinner = itertools.cycle(["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"])
    while not stop_event.is_set():
        print(f"\r{BLUE}Recherche en cours {next(spinner)}{RESET}", end="", flush=True)
        time.sleep(0.1)
    print("\r" + " " * 40 + "\r", end="")

def get_profile(username):
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False
    )
    with suppress_output():
        profile = instaloader.Profile.from_username(loader.context, username)
    return profile

def show_profile(profile):
    print(f"{BLUE}──────────────────────────────────────────────{RESET}")
    print(f"{BLUE}👤 Nom complet       : {profile.full_name}{RESET}")
    print(f"{BLUE}📛 Username          : {profile.username}{RESET}")
    print(f"{BLUE}🆔 ID Instagram      : {profile.userid}{RESET}")
    print(f"{BLUE}📝 Bio               : {profile.biography}{RESET}")
    print(f"{BLUE}🔗 Profil            : https://instagram.com/{profile.username}{RESET}")
    print(f"{BLUE}🖼️ Photo             : {profile.profile_pic_url}{RESET}")
    print(f"{BLUE}📷 Publications      : {profile.mediacount}{RESET}")
    print(f"{BLUE}👥 Abonnés           : {profile.followers}{RESET}")
    print(f"{BLUE}👣 Abonnements       : {profile.followees}{RESET}")
    print(f"{BLUE}✔️ Vérifié           : {'Oui' if profile.is_verified else 'Non'}{RESET}")
    print(f"{BLUE}🔒 Privé             : {'Oui' if profile.is_private else 'Non'}{RESET}")
    print(f"{BLUE}🏢 Compte Pro        : {'Oui' if profile.is_business_account else 'Non'}{RESET}")

    if profile.is_business_account:
        print(f"{BLUE}🏷️ Catégorie Pro     : {profile.business_category_name}{RESET}")

    print(f"{BLUE}──────────────────────────────────────────────{RESET}")

    if not profile.is_private:
        try:
            for i, post in enumerate(profile.get_posts()):
                print(f"{BLUE}📌 Post {i+1}{RESET}")
                print(f"{BLUE}🔗 https://www.instagram.com/p/{post.shortcode}/{RESET}")
                print(f"{BLUE}📅 Date        : {post.date}{RESET}")
                print(f"{BLUE}❤️ Likes       : {post.likes}{RESET}")
                print(f"{BLUE}💬 Commentaires: {post.comments}{RESET}")
                print(f"{BLUE}📝 Légende     : {post.caption if post.caption else 'Aucune'}{RESET}")
                print(f"{BLUE}──────────────────────────────────────────────{RESET}")
                if i == 4:
                    break
        except:
            pass
    else:
        print(f"{BLUE}🔒 Compte privé : posts non accessibles{RESET}")

if __name__ == "__main__":
    while True:
        clear_console()
        username = input(f"{BLUE}🔎 Username Instagram: {RESET}").strip()
        if not username:
            print(f"{BLUE}Au revoir !{RESET}")
            break

        stop_event = threading.Event()
        t = threading.Thread(target=loading_animation, args=(stop_event,))
        t.start()

        try:
            profile = get_profile(username)
        except:
            stop_event.set()
            t.join()
            print(f"{BLUE}❌ Username introuvable{RESET}")
            time.sleep(1.5)
            continue

        stop_event.set()
        t.join()

        clear_console()
        show_profile(profile)

        nxt = input(f"\n{BLUE}Entrée revenir au menu: {RESET}").strip()
        if not nxt:
            print(f"{BLUE}Au revoir !{RESET}")
            break
