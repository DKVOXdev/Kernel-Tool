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
import shutil
import time
import math
import subprocess
import io
import webbrowser
import builtins

try:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Program'))
    from Config.Config import *
    from Config.Util import *
except Exception as e:
    print(f"Error importing config: {e}")
    os_name = "Windows" if os.name == 'nt' else "Linux"
    tool_path = os.path.dirname(os.path.abspath(__file__))
    def Clear():
        try:
            os.system("cls" if os_name == "Windows" else "clear")
        except:
            pass

try:
    from rich.console import Console, Group
    from rich.live import Live
    from rich.text import Text
    from rich.align import Align
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

os.system('')

try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except:
    pass

ascii_art = [
    "██╗░░██╗███████╗██████╗░███╗░░██╗███████╗██╗░░░░░",
    "██║░██╔╝██╔════╝██╔══██╗████╗░██║██╔════╝██║░░░░░",
    "█████═╝░█████╗░░██████╔╝██╔██╗██║█████╗░░██║░░░░░",
    "██╔═██╗░██╔══╝░░██╔══██╗██║╚████║██╔══╝░░██║░░░░░",
    "██║░╚██╗███████╗██║░░██║██║░╚███║███████╗███████╗",
    "╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝╚═╝░░╚══╝╚══════╝╚══════╝"
]

start_color = (255, 30, 30)
end_color = (60, 0, 0)
gradient_length = len(ascii_art)

def interpolate(start, end, step, total):
    r = int(start[0] + (end[0] - start[0]) * step / total)
    g = int(start[1] + (end[1] - start[1]) * step / total)
    b = int(start[2] + (end[2] - start[2]) * step / total)
    return r, g, b

def colored_print(text, r, g, b):
    print(f"\033[38;2;{r};{g};{b}m{text}\033[0m")

def get_logo_rich():
    if not RICH_AVAILABLE:
        return None
    logo = Text(justify="center")
    for i, line in enumerate(ascii_art):
        r, g, b = interpolate(start_color, end_color, i, gradient_length - 1) if i < gradient_length else end_color
        logo.append(line, style=f"rgb({r},{g},{b})")
        logo.append("\n")
    logo.append("\nKernel Tool ● V1\n")
    return logo

def print_logo():
    try:
        w = shutil.get_terminal_size().columns
        h = shutil.get_terminal_size().lines
    except:
        w = h = 80
    logo_h = len(ascii_art) + 4
    top_pad = max(0, (h - logo_h) // 2)
    if top_pad:
        print("\n" * top_pad, end="")
    print("\n")
    for i, line in enumerate(ascii_art):
        pad = (w - len(line)) // 2
        centered = " " * pad + line
        r, g, b = interpolate(start_color, end_color, i, gradient_length - 1) if i < gradient_length else end_color
        colored_print(centered, r, g, b)
    print("\n")
    link = "https://guns.lol/2437"
    pad = (w - len(link)) // 2
    print(" " * pad + link)
    print("\n")

OPTIONS = {
    '01': 'Website-Strength-Scanner',
    '02': 'Website-Status',
    '03': 'Arpspoofing',
    '10': 'Rat-Bluid',
    '11': 'Grabber-Build',
    '12': 'Stealer-Build',
    '20': 'Cookie-Login',
    '21': 'Pseudo-Info',
    '30': 'Nitro-Gen',
    '31': 'Token-Info',
    '32': 'Token-Login',
    '33': 'Token-Server-Join',
    '34': 'Token-Block-Friends',
    '35': 'Token-Change-Language',
    '36': 'Delete-Webhook',
    '37': 'Webhook-Spammer',
    '38': 'Discord-Nuker',
    '40': 'Ip-Lookup',
    '41': 'Mail-Info',
    '42': 'Phone-Lookup',
    '43': 'Username-Tracker',
    '44': 'Instagram-Tracker',
    '45': 'Lookup-Ghitub',
    '46': 'Fake-Identite',
    '50': 'iban-generator',
    '51': 'fakevoice',
    '52': 'usb-tool',
    '53': 'exe-to-image',

}

MENU_PAGES = {
    '1': {
        'title': ' Network ',
        'categories': [{'title': ' Network ', 'options': ['01', '02','03'], 'color': '#FF4444'}]
    },
    '2': {
        'title': ' OSINT ',
        'categories': [{'title': ' OSINT & Recon ', 'options': ['40','41','42','43','44','45','46'], 'color': '#00D4FF'}]
    },
    '3': {
        'title': ' Roblox ',
        'categories': [{'title': ' Roblox ', 'options': ['20', '21'], 'color': '#FF8844'}]
    },
    '4': {
        'title': ' Discord ',
        'categories': [{'title': ' Discord ', 'options': ['30','31','32','33','34','35','36','37','38'], 'color': '#FFD700'}]
    },
    '5': {
        'title': ' Scam ',
        'categories': [{'title': ' Scam ', 'options': ['50','51','52','53'], 'color': '#FF0000'}]
    },
    '6': {
        'title': ' Paid ',
        'categories': [{'title': ' Malware Build ', 'options': ['10','11','12'], 'color': '#4444FF'}]
    }
}

BASE_BOX_WIDTH = 45
MIN_BOX_WIDTH = 28
FPS = 30
FLOW_SPEED = 0.25
VIS_THRESHOLD = 0.35
BOX_SPACING = "   "

def wave(step, offset=0.0):
    return (math.sin(step * FLOW_SPEED + offset) + 1) / 2

def animated_hline(length, step, offset=0.0):
    if not RICH_AVAILABLE:
        return "─" * length
    return "".join("─" if wave(step, i * 0.15 + offset) > VIS_THRESHOLD else " " for i in range(length))

def get_option_color(opt_num):
    for page in MENU_PAGES.values():
        for cat in page['categories']:
            if opt_num in cat['options']:
                return cat['color']
    return '#FFFFFF'

def format_option_text(opt_num, max_width=30, color=None):
    name = OPTIONS.get(opt_num, 'Unknown').replace('-', ' ')
    text = f"[{opt_num}] {name}"
    return Text(text, style=color) if color and RICH_AVAILABLE else text

def render_box(step, category, box_width, page_num):
    color = category['color']
    if not RICH_AVAILABLE:
        lines = [f"╭{'─'*(box_width-2)}╮", f"│{category['title'].center(box_width-2)}│"]
        for o in category.get('options', []):
            lines.append(f"│{format_option_text(o, box_width-6).ljust(box_width-2)}│")
        if not category.get('options'):
            lines.append(f"│{'No options available'.center(box_width-2)}│")
        lines.append(f"╰{'─'*(box_width-2)}╯")
        return lines

    lines = []
    title = category['title']
    opts = category.get('options', [])

    top = Text("╭", style=color) + Text(animated_hline(box_width-2, step), style=color)
    title_pos = (box_width - len(title)) // 2 - 1
    if title_pos >= 0:
        before = top[:title_pos+1]
        after = top[title_pos+1+len(title):]
        top = before + Text(title, style=color) + after
    top += Text("╮", style=color)
    lines.append(top)

    for i, opt in enumerate(opts):
        txt = format_option_text(opt, box_width-6, color)
        txt_str = txt.plain if isinstance(txt, Text) else str(txt)
        pad = box_width - 2 - len(txt_str)
        left = "│" if wave(step, i) > VIS_THRESHOLD else " "
        right = "│" if wave(step, i + 1.5) > VIS_THRESHOLD else " "
        line = Text(left, style=color) + (txt if isinstance(txt, Text) else Text(txt, style=color))
        if pad > 0:
            line += Text(" " * pad, style=color)
        line += Text(right, style=color)
        lines.append(line)

    if not opts:
        msg = "No options available"
        pad = box_width - 2 - len(msg)
        line = Text("│", style=color) + Text(msg.center(box_width-2), style=color) + Text("│", style=color)
        lines.append(line)

    bottom = Text("╰", style=color) + Text(animated_hline(box_width-2, step, 2.0), style=color) + Text("╯", style=color)
    lines.append(bottom)
    return lines

def _get_menu_layout(cats):
    try:
        w = shutil.get_terminal_size().columns
    except:
        w = 80
    n = len(cats)
    spacing = len(BOX_SPACING)
    if n == 1:
        bw = min(70, max(BASE_BOX_WIDTH, w - 10))
        return {"mode": "horizontal", "box_width": bw}
    min_total = MIN_BOX_WIDTH * n + spacing * (n - 1)
    if w < min_total:
        return {"mode": "vertical", "box_width": min(BASE_BOX_WIDTH, max(MIN_BOX_WIDTH, w - 4))}
    avail = w - spacing * (n - 1)
    bw = max(MIN_BOX_WIDTH, min(BASE_BOX_WIDTH, avail // n))
    return {"mode": "horizontal", "box_width": bw}

def render_menu(step, page_num):
    if not RICH_AVAILABLE:
        return None
    page = MENU_PAGES.get(page_num, MENU_PAGES['1'])
    cats = page['categories']
    layout = _get_menu_layout(cats)
    bw = layout["box_width"]
    boxes = [render_box(step, cat, bw, page_num) for cat in cats]
    frame = Text()
    try:
        tw = shutil.get_terminal_size().columns
    except:
        tw = 80
    nav = f"Page {page_num}/6 | [N] Next | [B] Back | [I] Info"
    frame.append(nav.center(tw), style="dim")
    frame.append("\n\n")
    max_r = max(len(b) for b in boxes) if boxes else 3
    max_r = max(max_r, 3)
    for row in range(max_r):
        if len(boxes) == 1:
            b = boxes[0]
            pad = max(0, (tw - bw) // 2)
            frame.append(" " * pad)
            frame.append(b[row] if row < len(b) else Text(" " * bw))
        else:
            total_w = sum(bw for _ in boxes) + (len(boxes)-1) * len(BOX_SPACING)
            pad = max(0, (tw - total_w) // 2)
            if pad > 0:
                frame.append(" " * pad)
            for i, b in enumerate(boxes):
                frame.append(b[row] if row < len(b) else Text(" " * bw))
                if i < len(boxes)-1:
                    frame.append(BOX_SPACING)
        if row < max_r - 1:
            frame.append("\n")
    return frame

def display_animated_menu(page='1'):
    try:
        print("\033[2J\033[H", end="", flush=True)
        os.system("cls" if os.name == 'nt' else "clear")
    except:
        pass
    if RICH_AVAILABLE:
        try:
            console = Console(force_terminal=True)
            logo = get_logo_rich()
            with Live(refresh_per_second=FPS, screen=True, transient=False) as live:
                for step in range(30):
                    menu = render_menu(step, page)
                    if menu:
                        live.update(Align.center(Group(Align.center(logo) if logo else Text(), Align.center(menu))))
                    time.sleep(1/FPS)
                final = render_menu(30, page)
                if final:
                    live.update(Align.center(Group(Align.center(logo) if logo else Text(), Align.center(final))))
                    time.sleep(0.1)
            if final := render_menu(30, page):
                console.print(Align.center(Group(Align.center(logo) if logo else Text(), Align.center(final))))
        except:
            print_logo()
            display_simple_menu(page)
    else:
        print_logo()
        display_simple_menu(page)

def display_simple_menu(page='1'):
    try:
        w = shutil.get_terminal_size().columns
    except:
        w = 80
    cfg = MENU_PAGES.get(page, MENU_PAGES['1'])
    print(f"\n{cfg['title'].center(w)}")
    print(f"Page {page}/6 | [N] Next | [B] Back | [I] Info".center(w))
    print()
    for cat in cfg['categories']:
        print("\n" + cat['title'].center(w))
        color = cat['color']
        hex_c = color.lstrip('#')
        r,g,b = int(hex_c[0:2],16), int(hex_c[2:4],16), int(hex_c[4:6],16)
        for opt in cat.get('options', []):
            txt = format_option_text(opt)
            print(("  " + f"\033[38;2;{r};{g};{b}m{txt}\033[0m").center(w))
        if not cat.get('options'):
            print(("  No options available").center(w))

class ColorFilter:
    def __init__(self, original, rgb):
        self.original = original
        self.color = f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
        self.reset = "\033[0m"

    def write(self, text):
        if text:
            self.original.write(self.color)
            self.original.write(text)
            if text.endswith(('\n', '\r\n')):
                self.original.write(self.reset)

    def flush(self):
        self.original.flush()

    def __getattr__(self, name):
        return getattr(self.original, name)

def start_program(name):
    try:
        key = next(k for k,v in OPTIONS.items() if v == name)
        col_hex = get_option_color(key).lstrip('#')
        rgb = (int(col_hex[0:2],16), int(col_hex[2:4],16), int(col_hex[4:6],16))
    except:
        rgb = (200, 200, 200)

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Program", f"{name}.py")
    if not os.path.exists(path):
        print(f"[!] File not found : {name}.py")
        print(f"    Path: {path}")
        input("\nEnter to continue...")
        return

    old_out = sys.stdout
    old_err = sys.stderr
    old_input = builtins.input

    filter_out = ColorFilter(old_out, rgb)
    filter_err = ColorFilter(old_err, rgb)
    sys.stdout = filter_out
    sys.stderr = filter_err

    def input_color(prompt=''):
        if prompt:
            sys.stdout.write(str(prompt))
            sys.stdout.flush()
        return old_input('')

    builtins.input = input_color

    old_run = subprocess.run
    def safe_run(*a, **kw):
        if a and 'kernel.py' in str(a[0]):
            sys.exit(0)
        return old_run(*a, **kw)
    subprocess.run = safe_run

    def kill_reset():
        sys.exit(0)

    try:
        dir_script = os.path.dirname(path)
        old_cwd = os.getcwd()
        old_path = sys.path[:]
        if dir_script not in sys.path:
            sys.path.insert(0, dir_script)
        os.chdir(dir_script)

        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            code = f.read()

        ns = {'__name__': '__main__', '__file__': path, '__package__': None}
        exec(compile(code, path, 'exec'), ns)

        if 'Config' in ns and hasattr(ns['Config'], 'Util'):
            u = ns['Config'].Util
            if hasattr(u, 'Reset'):
                u.Reset = kill_reset

    except SystemExit:
        pass
    except Exception as e:
        print(f"[!] Execution error: {e}")
    finally:
        os.chdir(old_cwd)
        sys.path[:] = old_path
        sys.stdout = old_out
        sys.stderr = old_err
        builtins.input = old_input
        subprocess.run = old_run

    Clear()

menu_number = '1'
tool_path = os.path.dirname(os.path.abspath(__file__))
menu_file = os.path.join(tool_path, "Program", "Config", "Menu.txt")

try:
    if os.path.exists(menu_file):
        with open(menu_file) as f:
            val = f.read().strip()
            if val in MENU_PAGES:
                menu_number = val
except:
    pass

while True:
    try:
        os.system("title Kernel_tools")
    except:
        pass
    display_animated_menu(menu_number)
    print("")
    w = shutil.get_terminal_size().columns if shutil.get_terminal_size() else 80
    choice = input(f"Option: ".center(w // 2)).strip().lower()

    if choice in ('n', 'next'):
        menu_number = {"1":"2", "2":"3", "3":"4", "4":"5", "5":"6", "6":"1"}.get(menu_number, "1")
        try:
            with open(menu_file, "w") as f:
                f.write(menu_number)
        except:
            pass
        continue

    if choice in ('b', 'back'):
        menu_number = {"2":"1", "3":"2", "4":"3", "5":"4", "6":"5", "1":"6"}.get(menu_number, "1")
        try:
            with open(menu_file, "w") as f:
                f.write(menu_number)
        except:
            pass
        continue

    if choice in ('i', 'info'):
        webbrowser.open("https://discord.gg/jkz5Gn6rMs")
        webbrowser.open("https://guns.lol/2437")
        continue

    if choice in ('exit', 'quit', 'q'):
        break

    if choice in OPTIONS:
        start_program(OPTIONS[choice])
        continue

    if len(choice) == 1 and choice.isdigit():
        page = MENU_PAGES.get(menu_number, MENU_PAGES['1'])
        has_zero = any(opt.startswith('0') for cat in page['categories'] for opt in cat['options'])
        if has_zero:
            padded = '0' + choice
            if padded in OPTIONS:
                start_program(OPTIONS[padded])
                continue

    print("[!] Invalid choice.")
    time.sleep(1)
