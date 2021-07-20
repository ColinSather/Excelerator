import pandas as pd
from configparser import ConfigParser
from datetime import datetime
import sys, os, csv

from excel_convert import ExcelFormat

from pathlib import Path # if using Windows

title = r"""
 /$$$$$$$$                               /$$                                /$$                        
| $$_____/                              | $$                               | $$                        
| $$       /$$   /$$  /$$$$$$$  /$$$$$$ | $$  /$$$$$$   /$$$$$$  /$$$$$$  /$$$$$$    /$$$$$$   /$$$$$$ 
| $$$$$   |  $$ /$$/ /$$_____/ /$$__  $$| $$ /$$__  $$ /$$__  $$|____  $$|_  $$_/   /$$__  $$ /$$__  $$
| $$__/    \  $$$$/ | $$      | $$$$$$$$| $$| $$$$$$$$| $$  \__/ /$$$$$$$  | $$    | $$  \ $$| $$  \__/
| $$        >$$  $$ | $$      | $$_____/| $$| $$_____/| $$      /$$__  $$  | $$ /$$| $$  | $$| $$      
| $$$$$$$$ /$$/\  $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$| $$     |  $$$$$$$  |  $$$$/|  $$$$$$/| $$      
|________/|__/  \__/ \_______/ \_______/|__/ \_______/|__/      \_______/   \___/   \______/ |__/     
"""

subtitle = "Version 1.0.0\n"
print(title)                                                                                      
print(subtitle)


# FIND CATEGORIES FOR A TRANSACTION DESCRIPTION [WIP].
#def find_categories(df):
#    sectiond = df[["Description", "Category"]]
#    arr = sectiond.to_dict("series")
#    csv_row = ""
#    
#    for i, j in zip(arr["Description"], arr["Category"]):
#        csv_row += str(i) + "," + str(j) + "\n"
#
#    csv_row = csv_row[:len(csv_row) -2]
#    return arr

# WRITE ERRORS TO A TEXT FILE.
#def error_logger():
#    # TODO: implement an error log file [WIP]
#    cwd = os.path.abspath(os.path.dirname(__file__))
#    given_path = "./config/error.log"
#    error_log = os.path.abspath(os.path.join(cwd, given_path))
#    logf = open(error_log, "w")
#


#def run_merge():
#    try:
#        cwd = os.path.abspath(os.path.dirname(__file__))
#        given_path = "./config/config.ini"
#        config_file_path = os.path.abspath(os.path.join(cwd, given_path))
#
#        config = ConfigParser()
#        config.read(config_file_path)
#        master_file = config["PATHS"]["MasterFile"]
#        output_file = config["PATHS"]["OutputFile"]
#        
#        # Prepare the master file to be appended by the selected csv
#        main_master_file = master_file
#        main_output_file = output_file
#        in_file = sys.argv[1]
#
#        append_to_master(main_master_file, in_file)
#
#    except:
#        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), "excelerator was not able to import the selected csv to the master file.")
#        #logf.write(str(e)+"\n")
#        return False


class CSV_Controller:
    
    def load_import_files(self, dir):
        # load available files in config parser imports
        available_imports = []
        for file in os.listdir(dir):
            available_imports.append(file)
        return available_imports
        
    def date_sort(self, file_path):
        # Sort by the date field in the first column (cannot change col 1 of csv schema)
        data = pd.read_csv(file_path)
        cols = list(data.columns)
        data.sort_values(by = cols[0], ascending = False, inplace = True)
        data.to_csv(file_path, index=False)

    def add_to_main(self, main_file, in_file):
        # read main file and in_file as new dataframes
        a = pd.read_csv(main_file, index_col=False)
        b = pd.read_csv(in_file, index_col=False)
        frames = [a, b]
        result = pd.concat(frames, ignore_index=True)
        result.to_csv(main_file, index=False)
        os.remove(in_file)
        
    def assign_categories(self, df):
        # TODO: match categories or at least make it easier to input
        pass

    def display_csv(self, df):
        # TODO: display csv file, similar to GitHub's style
        pass


# MAIN EXECUTION SECTION
if __name__ == "__main__":
    # Commented out code was used when Excelerator could be ran from Windows context menu,
    # I may bring this feature back.

    # run_merge() # overly confusing method
    # TODO: Assign categories to the appended transactions
    # print("SUCCESS: The file", sys.argv[1], "has been appended to the master file.")
    # print("\n[WIP] The following transaction descriptions have been assigned to these categories...")

    # CLI options: open, history, shell
    # print("\nADDITIONAL OPERATIONS:")
    # print("open - opens the output file in your default spreadsheet program.")
    # print("history - shows files and dates that have been appended to the master file.")
    # print("quit - exits this program or you can simply hit the enter key.")
    # menu_option = input("Type one of the above options...\n")
    # 
    # if menu_option == "open" and platform.system() == "Windows":
    #     os.startfile(main_output_file)
    # if menu_option == "quit":
    #     print("Bye.")

    cwd = os.path.abspath(os.path.dirname(__file__))
    given_path = "./config.ini"
    config_file_path = os.path.abspath(os.path.join(cwd, given_path))

    config = ConfigParser()
    config.read(config_file_path)
    imports_dir = config._sections["imports"]["path"]
    accounts = config._sections["accounts"]
    acct_keys = list(accounts.keys())
    active_account = acct_keys[0]
    active_import = None
    available_imports = []

    print("Available Imports:")
    cc = CSV_Controller()
    ai = cc.load_import_files(imports_dir)
    
    if len(ai) == 0:
        print("No files in: ", imports_dir, "\n")
    else:
        active_import = ai[0]
        counter = 0
        for file in ai:
            print("[{}]".format(counter), file)
            counter += 1
        print()

    flag = True

    while flag:
        x = input("E-Shell> ")
        if x == "ls" or x == "show accounts":
            for key in accounts.keys():
                print(key)

        elif "use" in x.split():
            if x.split()[1] in accounts.keys():
                active_account = x.split()[1]
                print("switched to", x.split()[1])
            
            elif x.split()[1] in ai:
                active_import = x.split()[1]
                print("switched import to", x.split()[1])
            else:
                print("Invalid `use` command, please specify a correct account or file to import.")
                
        elif x == "sort":
            # This function always sorts the file in use
            cc.date_sort(accounts[active_account])

        elif "add" in x.split():
            if x.split()[1]:
                selected_index = int(x.split()[1])
                in_file = imports_dir+active_import
                cc.add_to_main(accounts[active_account], in_file)
                ai.remove(active_import)
            else:
                print("Invalid use of `add` command, please specify a correct export name.")

        elif x == "imports" or x == "show imports":
            counter = 0
            for file in ai:
                print("[{}]".format(counter), file)
                counter += 1

        elif x == "exit":
            print("Bye.")
            flag = False
