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
import sys
import time
try:
    from selenium import webdriver
except Exception as e:
    ErrorModule(e)

Title("Token Login")
try:      
    discord_token = Choice1TokenDiscord()

    print(f"""
 {BEFORE}01{AFTER}{white} Chrome (Windows / Linux)
 {BEFORE}02{AFTER}{white} Edge (Windows)
 {BEFORE}03{AFTER}{white} Firefox (Windows)
    """)
    selected_browser = input(f"{BEFORE + AFTER} {INPUT} Browser -> {reset}")
 
    if selected_browser in ['1', '01']:
        try:
            browser_name = "Chrome"
            print(f"{BEFORE + AFTER} {WAIT} {browser_name} Starting..{blue}")
            driver = webdriver.Chrome()
            print(f"{BEFORE + AFTER} {INFO} {browser_name} Ready !{blue}")
        except:
            print(f"{BEFORE + AFTER} {ERROR} {browser_name} not installed or driver not up to date.")
            Continue()
            Reset()

    elif selected_browser in ['2', '02']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                browser_name = "Edge"
                print(f"{BEFORE + AFTER} {WAIT} {browser_name} Starting..{blue}")
                driver = webdriver.Edge()
                print(f"{BEFORE + AFTER} {INFO} {browser_name} Ready !{blue}")
            except:
                print(f"{BEFORE + AFTER} {ERROR} {browser_name} not installed or driver not up to date.")
                Continue()
                Reset()

    elif selected_browser in ['3', '03']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                browser_name = "Firefox"
                print(f"{BEFORE + AFTER} {WAIT} {browser_name} Starting..{blue}")
                driver = webdriver.Firefox()
                print(f"{BEFORE + AFTER} {INFO} {browser_name} Ready !{blue}")
            except:
                print(f"{BEFORE + AFTER} {ERROR} {browser_name} not installed or driver not up to date.")
                Continue()
                Reset()
    else:
        ErrorChoice()
    
    try:
        login_script = """
                function login(token) {
                setInterval(() => {
                document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
                }, 50);
                setTimeout(() => {
                location.reload();
                }, 2500);
                }
                """
        
        driver.get("https://discord.com/login")
        print(f"{BEFORE + AFTER} {WAIT} Establishing Token Connection..{blue}")
        driver.execute_script(login_script + f'
login("{discord_token}")')
        time.sleep(4)
        print(f"{BEFORE + AFTER} {INFO} Token Successfully Connected !{blue}")
        print(f"{BEFORE + AFTER} {INFO} If you exit the tool, {browser_name} will close!{blue}")
        Continue()
        Reset()
    except:
        print(f"{BEFORE + AFTER} {ERROR} {browser_name} not installed or driver not up to date.")
        Continue()
        Reset()
except Exception as e:
    Error(e)
