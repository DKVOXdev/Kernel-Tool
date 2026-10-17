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
import sys
import time

try:
    from selenium import webdriver
except Exception as e:
    ErrorModule(e)

_ = "\033[96m"
_r = "\033[0m"

Title("Cookie Login")
Reset()
print(cookie_login_banner)

try:
    roblox_cookie = input(f"\n{_} {INPUT} Cookie -> {_r}")
    print(f"\n{_} 01 Chrome (Windows / Linux)")
    print(f"{_} 02 Edge (Windows)")
    print(f"{_} 03 Firefox (Windows)\n{_r}")
    selected_browser = input(f"{_} {INPUT} Browser -> {_r}")

    if selected_browser in ['1', '01']:
        try:
            browser_name = "Chrome"
            print(f"{_} {WAIT} {browser_name} Starting..{_r}")
            driver = webdriver.Chrome()
            print(f"{_} {INFO} {browser_name} Ready !{_r}")
        except Exception:
            print(f"{_} {ERROR} {browser_name} not installed or driver not up to date.{_r}")
            Continue()

    elif selected_browser in ['2', '02']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                browser_name = "Edge"
                print(f"{_} {WAIT} {browser_name} Starting..{_r}")
                driver = webdriver.Edge()
                print(f"{_} {INFO} {browser_name} Ready !{_r}")
            except Exception:
                print(f"{_} {ERROR} {browser_name} not installed or driver not up to date.{_r}")
                Continue()

    elif selected_browser in ['3', '03']:
        if sys.platform.startswith("linux"):
            OnlyLinux()
        else:
            try:
                browser_name = "Firefox"
                print(f"{_} {WAIT} {browser_name} Starting..{_r}")
                driver = webdriver.Firefox()
                print(f"{_} {INFO} {browser_name} Ready !{_r}")
            except Exception:
                print(f"{_} {ERROR} {browser_name} not installed or driver not up to date.{_r}")
                Continue()
    else:
        ErrorChoice()

    try:
        driver.get("https://www.roblox.com/Login")
        print(f"{_} {WAIT} Establishing Cookie Connection..{_r}")
        driver.add_cookie({"name": ".ROBLOSECURITY", "value": roblox_cookie})
        print(f"{_} {INFO} Cookie Successfully Connected !{_r}")
        print(f"{_} {WAIT} Refreshing The Page..{_r}")
        driver.refresh()
        print(f"{_} {INFO} Successfully Connected !{_r}")
        time.sleep(1)
        driver.get("https://www.roblox.com/users/profile")
        print(f"{_} {INFO} If you exit the tool, {browser_name} will close!{_r}")
        Continue()
    except Exception:
        print(f"{_} {ERROR} {browser_name} not installed or driver not up to date.{_r}")
        Continue()

except Exception as e:
    Error(e)
