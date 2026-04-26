# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ------------------------------------------------------------------------------>
# EN:
#     - Do not touch or modify the code below. If there is an error, please cont>
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez>
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import subprocess
import sys
from pathlib import Path
import os

GREEN = "\033[32m"
BOLD_GREEN = "\033[1;32m"
RESET = "\033[0m"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_green(text):
    print(f"{GREEN}{text}{RESET}")

def print_bold_green(text):
    print(f"{BOLD_GREEN}{text}{RESET}")

clear()

print_bold_green("=" * 60)
print_bold_green("          KERNEL TOOL - INSTALLER")
print_bold_green("=" * 60)
print()

requirements_file = "requirements.txt"
main_script = "kernel.py"

if not Path(requirements_file).exists():
    print_green(f"[!] File {requirements_file} not found.")
    sys.exit(1)

print_green("[*] Updating pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print_green("[✓] Pip updated successfully.")
except subprocess.CalledProcessError:
    print_green("[!] Unable to update pip, continuing...")

with open(requirements_file, "r", encoding="utf-8") as f:
    packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

if packages:
    for pkg in packages:
        print_green(f"[*] Installing {pkg}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print_green(f"[✓] {pkg} installed successfully.")
        except subprocess.CalledProcessError:
            print_green(f"[✗] Failed to install {pkg}")
else:
    print_green("[!] No modules to install in requirements.txt")

if not Path(main_script).exists():
    print_green(f"[!] Script {main_script} not found.")
    sys.exit(1)

print_green(f"[*] Launching {main_script}...\n")

os.system(f'"{sys.executable}" "{main_script}"')
