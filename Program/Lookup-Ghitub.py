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

import requests
from datetime import datetime
from collections import defaultdict
from Config.Config import *
from Config.Util import *

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
    return cached_fetch(f"https://api.github.com/users/{username}")

def get_email_from_commits(username):
    try:
        repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
        for repo in repos:
            commits = cached_fetch(f"https://api.github.com/repos/{username}/{repo['name']}/commits")
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
    lang_bytes = {}
    for repo in repos:
        languages_url = repo.get("languages_url")
        if languages_url:
            langs = cached_fetch(languages_url)
            if langs:
                for lang, bytes_count in langs.items():
                    lang_bytes[lang] = lang_bytes.get(lang, 0) + bytes_count
    sorted_langs = sorted(lang_bytes.items(), key=lambda x: x[1], reverse=True)
    top_langs = [lang for lang, _ in sorted_langs[:3]]
    return top_langs if top_langs else ["N/A"]

def count_total_stars(repos):
    return sum(repo.get("stargazers_count", 0) for repo in repos)

def count_starred_projects(username):
    starred = get_paginated_data(f"https://api.github.com/users/{username}/starred")
    return len(starred)

Title("Lookup Github")
Clear()
print(github_lookup_banner)

try:
    username = input(f"\033[96m {INPUT} GitHub Username -> \033[0m").strip()

    if not username:
        print(f"\033[96m {ERROR} No username entered.\033[0m")
        Continue()
        Clear()
    else:
        user = get_user_info(username)
        if not user:
            print(f"\033[96m {ERROR} User not found.\033[0m")
            Continue()
            Clear()
        else:
            name, email = get_email_from_commits(username)
            repos = get_paginated_data(f"https://api.github.com/users/{username}/repos")
            user_stars = count_total_stars(repos)
            projet_stars = count_starred_projects(username)
            top_languages = get_languages_stats(username)
            twitter = user.get("twitter_username")

            print(f"""
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
 {INFO_ADD} Username        : {user.get('login')}
 {INFO_ADD} Name            : {user.get('name')}
 {INFO_ADD} Email           : {email}
 {INFO_ADD} Public Repos    : {user.get('public_repos')}
 {INFO_ADD} Followers       : {user.get('followers')}
 {INFO_ADD} User Stars      : {user_stars}
 {INFO_ADD} Project Stars   : {projet_stars}
 {INFO_ADD} Top Languages   : {', '.join(top_languages)}
 {INFO_ADD} Location        : {user.get('location')}
 {INFO_ADD} Bio             : {user.get('bio')}
 {INFO_ADD} Company         : {user.get('company')}
 {INFO_ADD} Blog            : {user.get('blog')}
 {INFO_ADD} Twitter         : {"@" + twitter if twitter else "N/A"}
 {INFO_ADD} Created At      : {format_date(user.get('created_at'))}
 {INFO_ADD} Updated At      : {format_date(user.get('updated_at'))}
 {INFO_ADD} Avatar URL      : {user.get('avatar_url')}
 {INFO_ADD} GitHub URL      : {user.get('html_url')}
\033[96m────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
\033[0m""")

            Continue()
            Clear()

except Exception as e:
    Error(e)
