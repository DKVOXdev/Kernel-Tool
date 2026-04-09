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

if not Path(requirements_file).exists():
    print(f"[!] Fichier {requirements_file} introuvable.")
    sys.exit(1)

print("[*] Mise à jour de pip...")
try:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    print("[✓] Pip mis à jour.")
except subprocess.CalledProcessError:
    print("[!] Impossible de mettre à jour pip, on continue...")

with open(requirements_file, "r", encoding="utf-8") as f:
    packages = [line.strip() for line in f if line.strip() and not line.startswith("#")]

if packages:
    for pkg in packages:
        print(f"[*] Installation de {pkg}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
            print(f"[✓] {pkg} installé avec succès.")
        except subprocess.CalledProcessError:
            print(f"[✗] Échec de l'installation de {pkg}")
else:
    print("[!] Aucun module à installer dans requirements.txt")

if not Path(main_script).exists():
    print(f"[!] Script {main_script} introuvable.")
    sys.exit(1)

print(f"[*] Lancement de {main_script}...\n")
os.system(f'"{sys.executable}" "{main_script}"')
