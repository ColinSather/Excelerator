import pandas as pd
import configparser
import sys, os

class ExcelFormat:

    def get_config(self):
        # Fetch the path to the configuration file
        cwd = os.path.abspath(os.path.dirname(__file__))
        given_path = "./config/config.ini"
        config_file_path = os.path.abspath(os.path.join(cwd, given_path))

        # Create the config parser object and return the output file path.
        config = configparser.ConfigParser()
        config.read(config_file_path)
        out_file_path = config["PATHS"]["OutputFile"]
        return out_file_path


    def format_cols(self, df):
        # Fetch output file from config using XlsxWriter as the engine.
        out_file_path = self.get_config()
        writer = pd.ExcelWriter(out_file_path, engine='xlsxwriter')

        # Convert the dataframe to an XlsxWriter Excel object.
        df.to_excel(writer, sheet_name='Sheet1', index=False)

        # Get the xlsxwriter workbook and worksheet objects.
        workbook  = writer.book
        worksheet = writer.sheets['Sheet1']

        # Add some cell formats.
        money = workbook.add_format({'num_format': '$#,##0.00'})
        intform = workbook.add_format({'num_format': '0'})
        
        # Note: It isn't possible to format any cells that already have a format such
        # as the index or headers or any cells that contain dates or datetimes.

        # Set the column width and format.
        worksheet.set_column('A:A', 18)
        worksheet.set_column('B:B', 18, intform)
        worksheet.set_column('C:C', 18, intform)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 75)
        worksheet.set_column('F:F', 9, money)
        worksheet.set_column('G:G', 9, money)
        worksheet.set_column('I:I', 18)
        worksheet.set_column('J:J', 22)

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()