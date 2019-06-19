# Processing Adobe Analytics CSV files
# CSV Prettifier
# 
# - Input: path of raw CSV files.
# - Output: CSV (single sheet)/XLSX (multiple sheets) files with improved readability.
# Import required modules
import pandas as pd
import os
import glob

def CSV_prettifier(path):
    
    """
    Input: path of raw .csv files from adobe debugger extension.
    (i.e. path = '/Users/[username]/Downloads')
    Output: .xlsx file with individual sheets for every hit + summary sheet.
    """
    
    # Read all csv files in specified path.
    all_files = glob.glob1(path,"*csv")
    
    # Remove any csv files that aren't part of analytics output.
    for file in all_files:
        if file[0:24] != 'adobe-analytics-data-raw':
            all_files.remove(file)
        
    li = []
    di = {}
    
    # Read csv files to pandas and append to `li` for summary page and `di` for indiv sheets.
    for filename in all_files:
        x = path+ '/' +filename
        df = pd.read_csv(x, index_col=None, header=0, sep='~~', engine='python')
        df.set_index('Report Suite ID    ', inplace=True)
        li.append(df)
        
        # Setting the name of each sheet to the webpage name.
        if len(df.iloc[0][0]) <= 31:
            di.update({ df.iloc[0][0] : df})
        elif len(df.iloc[0][0]) > 31:
            di.update({ 'home' : df})
        
        # Delete raw csv file after use.
        os.remove(x)
    
    # Concat list of dataframes to generate summary page.
    frame = pd.concat(li, axis=1, sort='False')
    di.update({'Summary' : frame})
    
    writer = pd.ExcelWriter('ShawQA-sheets.xlsx', engine='xlsxwriter')
    
    # Write each sheet to .xlsx file.
    for sheet in di.keys():
        di[sheet].to_excel(writer, sheet_name=sheet, index=True)

    writer.save()
