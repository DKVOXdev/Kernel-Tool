# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import requests
import os
from colorama import Fore, Style, init
import fade
from datetime import datetime
from collections import defaultdict
import hashlib
import json

init(autoreset=True)

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def ascii_logo():
    logo = f"""\n
██╗   ██╗███████╗███████╗██████╗
██║   ██║██╔════╝██╔════╝██╔══██╗
██║   ██║███████╗█████╗  ██████╔╝
██║   ██║╚════██║██╔══╝  ██╔══██╗
╚██████╔╝███████║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝
    """
    print(fade.purpleblue(logo))

def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
    except:
        return date_str

def cached_fetch(url):
    try:
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

def get_paginated_data(url):
    results = []
    page = 1
    while True:
        paged_url = f"{url}?per_page=100&page={page}"
        data = cached_fetch(paged_url)
        if not data:
            break
        results.extend(data)
        if len(data) < 100:
            break
        page += 1
    return results

def get_user_info(username):
    url = f"https://api.github.com/users/{username}"
    return cached_fetch(url)

def get_email_from_commits(username):
    try:
        repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
        for repo in repos:
            commits_url = f"https://api.github.com/repos/{username}/{repo['name']}/commits"
            commits = cached_fetch(commits_url)
            if isinstance(commits, list) and commits:
                author = commits[0].get("commit", {}).get("author", {})
                email = author.get("email", "")
                name = author.get("name", "")
                if email:
                    return name, email
    except:
        pass
    return "N/A", "N/A"

def get_languages_stats(username):
    repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
    lang_bytes = defaultdict(int)
    for repo in repos:
        languages_url = repo.get("languages_url")
        if languages_url:
            langs = cached_fetch(languages_url)
            if langs:
                for lang, bytes_count in langs.items():
                    lang_bytes[lang] += bytes_count
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    top_langs = [lang for lang, _ in sorted_langs[:3]]
    return top_langs if top_langs else ["N/A"]

def count_total_stars(repos):
    return sum(repo.get("stargazers_count", 0) for repo in repos)

def count_starred_projects(username):
    starred = get_paginated_data(f"https://api.github.com/users/{username}/starred")
    return len(starred)

def main():
    clear_console()
    ascii_logo()
    username = input("🔎 Enter GitHub username: ").strip()
    if not username:
        print(Fore.RED + "❌ Aucun nom d'utilisateur entré.")
        return

    user = get_user_info(username)
    if not user:
        print(Fore.RED + "❌ Utilisateur non trouvé.")
        return

    name, email = get_email_from_commits(username)
    repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
    user_stars = count_total_stars(repos)
    projet_stars = count_starred_projects(username)
    top_languages = get_languages_stats(username)

    print(Fore.GREEN + "\n🚀 GitHub User Info:\n")
    print(f"👤 Username: {user.get('login')}")
    print(f"📝 Name: {user.get('name')}")
    print(f"📧 Email: {email}")
    print(f"📦 Public Repos: {user.get('public_repos')}")
    print(f"👥 Followers: {user.get('followers')}")
    print(f"⭐ User Stars: {user_stars}")
    print(f"⭐ Projet Stars: {projet_stars}")
    print(f"🌐 Top Languages: {','.join(top_languages)}")
    print(f"📍 Location: {user.get('location')}")
    print(f"🧾 Bio: {user.get('bio')}")
    print(f"💼 Company: {user.get('company')}")
    print(f"🔗 Blog: {user.get('blog')}")
    twitter = user.get("twitter_username")
    print(f"🐦 Twitter: @{twitter}" if twitter else "🐦 Twitter: N/A")
    print(f"🗓️ Created At: {format_date(user.get('created_at'))}")
    print(f"⏱️ Updated At: {format_date(user.get('updated_at'))}")
    print(f"🖼️ Avatar URL: {user.get('avatar_url')}")
    print(f"🔗 GitHub URL: {user.get('html_url')}")

    input("\n➡ Appuyez sur Entrée pour revenir au menu")

if __name__ == "__main__":
    main()
