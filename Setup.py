# Copyright (c) Kernel-Tool
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN:
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR:
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import subprocess
import sys
from pathlib import Path
import os

requirements_file = "requirements.txt"
main_script = "kernel.py"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

clear()

if not Path(requirements_file).exists():
    print(f"[!] File {requirements_file} not found.")
    sys.exit(1)

print("[*] Updating pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("[✓] Pip updated successfully.")
except subprocess.CalledProcessError:
    print("[!] Unable to update pip, continuing...")

with open(requirements_file, "r", encoding="utf-8") as f:
    packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

if packages:
    for pkg in packages:
        print(f"[*] Installing {pkg}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"[✓] {pkg} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"[✗] Failed to install {pkg}")
else:
    print("[!] No modules to install in requirements.txt")

if not Path(main_script).exists():
    print(f"[!] Script {main_script} not found.")
    sys.exit(1)

print(f"[*] Launching {main_script}...\n")
os.system(f'"{sys.executable}" "{main_script}"')
