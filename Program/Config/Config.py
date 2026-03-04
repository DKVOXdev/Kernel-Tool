import os

import sys



# Color codes

class color:

    RESET = "\033[0m"

    RED = "\033[91m"

    GREEN = "\033[92m"

    YELLOW = "\033[93m"

    BLUE = "\033[94m"

    MAGENTA = "\033[95m"

    CYAN = "\033[96m"

    WHITE = "\033[97m"



# ANSI color variables

BEFORE = "\033[0;37m"

AFTER = "\033[0m"

BEFORE_GREEN = "\033[0;32m"

AFTER_GREEN = "\033[0m"



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

white = "\033[97m"

green = "\033[92m"

red = "\033[91m"

blue = "\033[94m"

reset = "\033[0m"



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


