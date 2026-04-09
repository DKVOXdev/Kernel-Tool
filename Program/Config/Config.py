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



# Color codes

class color:

    RESET = "[0m"

    RED = "[91m"

    GREEN = "[92m"

    YELLOW = "[93m"

    BLUE = "[94m"

    MAGENTA = "[95m"

    CYAN = "[96m"

    WHITE = "[97m"



# ANSI color variables

BEFORE = "[0;37m"

AFTER = "[0m"

BEFORE_GREEN = "[0;32m"

AFTER_GREEN = "[0m"



# Status indicators

INFO = "[INFO]"

ERROR = "[ERROR]"

WAIT = "[WAIT]"

INPUT = "[INPUT]"

GEN_VALID = "[VALID]"

GEN_INVALID = "[INVALID]"

ADD = "[ADD]"

INFO_ADD = "[+]"



# Color variables

white = "[97m"

green = "[92m"

red = "[91m"

blue = "[94m"

reset = "[0m"



# Banners

sql_banner = """

╔══════════════════════════════════════════════════════════════╗

║                    Website Strength Scanner                   ║

╚══════════════════════════════════════════════════════════════╝

"""



discord_banner = """

╔══════════════════════════════════════════════════════════════╗

║                      Discord Tools                            ║

╚══════════════════════════════════════════════════════════════╝

"""



# Get tool path

tool_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



# OS name

os_name = "Windows" if os.name == 'nt' else "Linux"
