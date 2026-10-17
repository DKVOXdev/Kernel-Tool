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

from Config.Util import *
from Config.Config import *

try:
    import rarfile
    import pyzipper
    import string
    import tkinter
    from tkinter import filedialog
    from concurrent.futures import ThreadPoolExecutor
    import zipfile
    import os
except Exception as e:
    ErrorModule(e)

Clear()
print(zip_cracker_banner)

Title("Zip Cracked")

try:
    def ChooseZipRarFile():
        try:
            print(f"\n{LC}{current_time_hour()} {INPUT} Enter the path to the .zip or .rar file -> {RS}")
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                file = filedialog.askopenfilename(parent=root, title="Zip Cracked - Choose a file (.zip / .rar)", filetypes=[("ZIP/RAR files", "*.zip;*.rar"), ("ZIP files", "*.zip"), ("RAR files", "*.rar")])
            else:
                file = filedialog.askopenfilename(title="Zip Cracked - Choose a file (.zip / .rar)", filetypes=[("ZIP/RAR files", "*.zip;*.rar")])
            print(f"{LC}{current_time_hour()} {INFO} File path: {file}{RS}")
            return file
        except:
            return input(f"{LC}{current_time_hour()} {INPUT} Enter the path to the .zip or .rar file -> {RS}")

    def ChooseWordlistFile():
        try:
            print(f"\n{LC}{current_time_hour()} {INPUT} Select your wordlist file -> {RS}")
            if sys.platform.startswith("win"):
                root = tkinter.Tk()
                root.withdraw()
                root.attributes('-topmost', True)
                file = filedialog.askopenfilename(parent=root, title="Zip Cracked - Choose Wordlist", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            else:
                file = filedialog.askopenfilename(title="Zip Cracked - Choose Wordlist", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
            if file:
                print(f"{LC}{current_time_hour()} {INFO} Wordlist selected: {file}{RS}")
                return file
            else:
                print(f"{LC}{current_time_hour()} {ERROR} No wordlist selected.{RS}")
                Continue()
                Reset()
        except:
            return input(f"{LC}{current_time_hour()} {INPUT} Enter the path to the wordlist -> {RS}")

    def CountEncryptedFiles(file):
        count = 0
        try:
            if file.lower().endswith('.zip'):
                try:
                    with pyzipper.AESZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, pwd=b'wrongpassword')
                            except RuntimeError:
                                count += 1
                except:
                    with zipfile.ZipFile(file) as archive:
                        for info in archive.infolist():
                            if info.flag_bits & 0x1:
                                count += 1
            elif file.lower().endswith('.rar'):
                with rarfile.RarFile(file) as archive:
                    for filename in archive.namelist():
                        try:
                            archive.extract(filename, pwd='wrongpassword')
                        except rarfile.BadPassword:
                            count += 1
            return count
        except:
            return count

    def CheckPassword(file, password_test):
        global password_found
        try:
            if file.lower().endswith('.zip'):
                try:
                    with pyzipper.AESZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.extract(filename, pwd=password_test.encode())
                                password_found += 1
                                print(f"{LC}{current_time_hour()} {ADD} File: {filename} Password: {password_test}{RS}")
                                return True
                            except:
                                pass
                except:
                    with zipfile.ZipFile(file) as archive:
                        for filename in archive.namelist():
                            try:
                                archive.setpassword(password_test.encode())
                                archive.read(filename)
                                password_found += 1
                                print(f"{LC}{current_time_hour()} {ADD} File: {filename} Password: {password_test}{RS}")
                                return True
                            except:
                                pass
            elif file.lower().endswith('.rar'):
                with rarfile.RarFile(file) as archive:
                    for filename in archive.namelist():
                        try:
                            archive.extract(filename, pwd=password_test.encode())
                            password_found += 1
                            print(f"{LC}{current_time_hour()} {ADD} File: {filename} Password: {password_test}{RS}")
                            return True
                        except:
                            pass
            return password_found > 0
        except:
            return False

    def RandomCharacter(count):
        global generated_passwords, password_found, file
        try:
            threads_number = int(input(f"{LC}{current_time_hour()} {INPUT} Threads Number -> {RS}"))
            characters_number_min = int(input(f"{LC}{current_time_hour()} {INPUT} Password Characters Number Min -> {RS}"))
            characters_number_max = int(input(f"{LC}{current_time_hour()} {INPUT} Password Characters Number Max -> {RS}"))
        except:
            ErrorNumber()

        generated_passwords = set()
        password_found = 0
        all_characters = string.ascii_letters + string.digits + string.punctuation

        def GeneratePassword():
            return ''.join(random.choice(all_characters) for _ in range(random.randint(characters_number_min, characters_number_max)))

        def TestCracked():
            global generated_passwords, password_found
            while password_found < count:
                password_test = GeneratePassword()
                if password_test not in generated_passwords:
                    generated_passwords.add(password_test)
                    if CheckPassword(file, password_test):
                        if password_found == count:
                            Continue()
                            Reset()

        def Request():
            with ThreadPoolExecutor(max_workers=threads_number) as executor:
                executor.map(lambda _: TestCracked(), range(threads_number))

        print(f"{LC}{current_time_hour()} {WAIT} Brute force password cracking in progress.. (It can be long){RS}")
        while password_found < count:
            Request()

    def WorldList():
        global password_found, file
        password_found = 0

        file_path = ChooseWordlistFile()
        if not file_path or not os.path.isfile(file_path):
            print(f"{LC}{current_time_hour()} {ERROR} Wordlist invalide.{RS}")
            Continue()
            Reset()
            return

        print(f"{LC}{current_time_hour()} {WAIT} Attaque par worldlist en cours...{RS}")
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                for line in f:
                    password_test = line.strip()
                    if password_test:
                        if CheckPassword(file, password_test):
                            if password_found == count:
                                Continue()
                                Reset()
                                return
        except Exception as e:
            print(f"{LC}{current_time_hour()} {ERROR} Erreur lors de la lecture de la wordlist.{RS}")

        if not password_found:
            print(f"{LC}{current_time_hour()} {INFO} Aucune password trouvee dans cette worldlist.{RS}")
            Continue()
            Reset()

    print(f"{LC}{current_time_hour()} {INFO} Starting Zip Cracked...{RS}")
    file = ChooseZipRarFile()

    count = CountEncryptedFiles(file)
    print(f"{LC}{current_time_hour()} {INFO} Number of files protected by password: {count}{RS}")
    if count == 0:
        Continue()
        Reset()

    print(f"""
{LC} [01] Random Character
 [02] World List{RS}
    """)

    method = input(f"{LC}{current_time_hour()} {INPUT} Method -> {RS}")

    if method in ["01", "1"]:
        RandomCharacter(count)
    elif method in ["02", "2"]:
        WorldList()
    else:
        ErrorChoice()

except Exception as e:
    Error(e)
