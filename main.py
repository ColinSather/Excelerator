import pandas as pd
import configparser
import sys, os, platform, itertools
from excel_convert import ExcelFormat

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

# TODO: use better practices here such as OOP.
main_master_file = ""
main_output_file = ""


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

def merge_master_file(master_file, in_file):
    # Append selected file to the master file in a new dataframe
    a = pd.read_csv(master_file, index_col=False)
    b = pd.read_csv(in_file, index_col=False)

    len_row = len(b.loc[0])
    b.drop([0, len_row])
    out = a.append(b, ignore_index=False)

    formatter = ExcelFormat()
    formatter.format_cols(out)

    # TODO: use supervised learning libs to match categories (optional).
    #find_categories(b)

    with open(master_file, 'a', encoding='utf-8', newline = '\n') as f:
        out.to_csv(f, index=False)
        f.close()
    
    # TODO: Log merge in config file's history [WIP]
    #with open(config_file_path, 'a') as hist:
    #    data = in_file+","
    #    hist.write(data)
    #    hist.close()


def run_merge():
    try:
        cwd = os.path.abspath(os.path.dirname(__file__))
        given_path = "./config/config.ini"
        config_file_path = os.path.abspath(os.path.join(cwd, given_path))

        config = configparser.ConfigParser()
        config.read(config_file_path)
        master_file = config["PATHS"]["MasterFile"]
        output_file = config["PATHS"]["OutputFile"]
        
        # Prepare the master file to be appended by the selected csv
        main_master_file = master_file
        main_output_file = output_file
        in_file = sys.argv[1]

        merge_master_file(main_master_file, in_file)

    except:
        print('Error on line {}'.format(sys.exc_info()[-1].tb_lineno), "excelerator was not able to import the selected csv to the master file.")
        #logf.write(str(e)+"\n")
        return False



# MAIN EXECUTION SECTION
if __name__ == "__main__":
    try:
        run_merge()
        # TODO: Assign categories to the appended transactions
        print("SUCCESS: The file", sys.argv[1], "has been appended to the master file.")
        print("\n[WIP] The following transaction descriptions have been assigned to these categories...")

        # CLI options: open, history, shell
        print("\nADDITIONAL OPERATIONS:")
        print("open - opens the output file in your default spreadsheet program.")
        print("history - shows files and dates that have been appended to the master file.")
        print("quit - exits this program or you can simply hit the enter key.")
        menu_option = input("Type one of the above options...\n")

        if menu_option == "open" and platform.system() == "Windows":
            os.startfile(main_output_file)
        if menu_option == "quit":
            print("Bye.")
    except:
        menu_option = input("The program failed for some reason, type enter to confirm.\n")
        if menu_option == "quit":
            print("Bye.")