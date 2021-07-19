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
    def date_sort(self, file_path):
        data = pd.read_csv(file_path)
        data.sort_values(by = 'Date', ascending = False, inplace = True)
        return data

    def add_to_main(self, main_file, in_file):
        # read main file and in_file as new dataframes
        a = pd.read_csv(main_file, index_col=False)
        b = pd.read_csv(in_file, index_col=False)
        frames = [a, b]
        result = pd.concat(frames)
        pd.write_csv(result)

        # TODO: use supervised learning libs to match categories (optional).
        #find_categories(b)


# MAIN EXECUTION SECTION
if __name__ == "__main__":
    # Commented out code was used when Excelerator could be ran from Windows context menu

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
    given_path = "./config/config.ini"
    config_file_path = os.path.abspath(os.path.join(cwd, given_path))
    config = ConfigParser()
    config.read(config_file_path)
    flag = True

    cc = CSV_Controller()
    export_dir = config._sections["Exports"]["path"]
    accounts = config._sections["Accounts"]
    
    active_account = None
    active_export = None
    active_exports = []

    while flag:
        x = input("E-Shell> ")
        if x == "accounts" or x == "show accounts":
            for key in accounts.keys():
                print(key)

        elif "use" in x.split():
            if x.split()[1] in accounts.keys():
                active_account = x.split()[1]
                print("switched to", x.split()[1])
            else:
                print("Invalid `use` command, please specify a correct account.")
                
        elif x == "sort":
            # temp function
            exports = os.listdir(export_dir)
            tmp = cc.date_sort(export_dir+exports[0])
            print(tmp)

        elif "add" in x.split():
            if x.split()[1]:
                selected_index = int(x.split()[1])
                active_export = active_exports[selected_index]
                cc.add_to_main(active_account, active_export)
            else:
                print("Invalid use of `add` command, please specify a correct export name.")

        elif x == "exports" or x == "show exports":
            counter = 0
            for file in os.listdir(export_dir):
                print("[{}]".format(counter), file)
                active_exports.append(export_dir+file)
                counter += 1

        elif x == "exit":
            print("Bye.")
            flag = False
