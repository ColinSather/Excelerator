import pandas as pd
import configparser
from datetime import datetime
import sys, os, platform

title = """
 /$$$$$$$$                               /$$                                /$$                        
| $$_____/                              | $$                               | $$                        
| $$       /$$   /$$  /$$$$$$$  /$$$$$$ | $$  /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
| $$$$$   |  $$ /$$/ /$$_____/ /$$__  $$| $$ /$$__  $$ /$$__  $$|____  $$|_  $$_/   /$$__  $$ /$$__  $$
| $$__/    \  $$$$/ | $$      | $$$$$$$$| $$| $$$$$$$$| $$  \__/ /$$$$$$$  | $$    | $$  \ $$| $$  \__/
| $$        >$$  $$ | $$      | $$_____/| $$| $$_____/| $$      /$$__  $$  | $$ /$$| $$  | $$| $$      
| $$$$$$$$ /$$/\  $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$| $$     |  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
|________/|__/  \__/ \_______/ \_______/|__/ \_______/|__/      \_______/   \___/   \______/ |__/     
"""
subtitle = "Version 1.0\n"

print(title)                                                                                      
print(subtitle)

cwd = os.path.abspath(os.path.dirname(__file__))
given_path = "./config/error.log"
error_log = os.path.abspath(os.path.join(cwd, given_path))
logf = open(error_log, "w")

try:
    in_file = sys.argv[1]
    config = configparser.ConfigParser()

    cwd = os.path.abspath(os.path.dirname(__file__))
    given_path = "./config/config.ini"
    master_file_path = os.path.abspath(os.path.join(cwd, given_path))

    config.read(master_file_path)
    master_file = config["PATH"]["MasterFile"]
    
    a = pd.read_csv(master_file)
    b = pd.read_csv(in_file)
    len_row = len(b.loc[0])
    b.drop([0, len_row])
    out = a.append(b)

    dt = str(datetime.now().replace(second=0, microsecond=0))
    mod_dt = dt.strip(":00")
    dt_arr = mod_dt.split()


    with open(master_file, 'w', encoding='utf-8', newline = '\n') as f:
        out.to_csv(f, index=False)
        print("The file", sys.argv[0], "has been appended to", master_file)
        f.close()

    with open(master_file_path, 'a') as hist:
        data = "\n"+dt_arr[0]+": "
        data += sys.argv[1]
        hist.write(data)
        hist.close()

except Exception as e:
    print("Error: excelerator was not able to import the selected csv to the master file.")
    print(str(e))
    if e.code == 12:
        print("Make sure the import file isn't open.")
    logf.write(str(e)+"\n")

# TODO: Assign categories to the appended transactions
print("The following transactions have been assigned to these categories...\n")

# CLI options: open, history, shell
print("\nopen - opens the master file in your default spreadsheet program.")
print("history - shows files and dates that have been appended to the master file.")
print("quit - exits this program or you can simply hit the enter key.")
menu_option = input("Type one of the above options...\n")

if menu_option == "open" and platform.system() == "Windows":
    os.startfile(master_file)

if menu_option == "quit":
    print("Bye.")