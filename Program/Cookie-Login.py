from Config.Util import *
from Config.Config import *
import sys
import time
try:
    from selenium import webdriver
except Exception as e:
    ErrorModule(e)

Title("Cookie Login")

try:
    roblox_cookie = input(f"\n{BEFORE + AFTER} {INPUT} Cookie -> {white}")
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
        driver.get("https://www.roblox.com/Login")
        print(f"{BEFORE + AFTER} {WAIT} Establishing Cookie Connection..{blue}")
        driver.add_cookie({"name" : ".ROBLOSECURITY", "value" : f"{roblox_cookie}"})
        print(f"{BEFORE + AFTER} {INFO} Cookie Successfully Connected !{blue}")
        print(f"{BEFORE + AFTER} {WAIT} Refreshing The Page..{blue}")
        driver.refresh()
        print(f"{BEFORE + AFTER} {INFO} Successfully Connected !{blue}")
        time.sleep(1)
        driver.get("https://www.roblox.com/users/profile")
        print(f"{BEFORE + AFTER} {INFO} If you exit the tool, {browser_name} will close!{blue}")
        Continue()
        Reset()
    except:
        print(f"{BEFORE + AFTER} {ERROR} {browser_name} not installed or driver not up to date.")
        Continue()
        Reset()
except Exception as e:
    Error(e)

