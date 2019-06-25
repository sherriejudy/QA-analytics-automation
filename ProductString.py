# Parsing Product String

# Import required modules
import pandas as pd
import os
import glob
from pathlib import Path

def productString(path, fileName):


    # Read all xlsx files in specified path.
    allFiles = glob.glob1(path, "*xlsx")

    # Remove any xlsx files that aren't part of form analytics
    for file in all_files:
        if file[0:len(finalName)] != finalName:
            # Remove from files list
            allFiles.remove(file)

    allFiles.sort()

    # Take the latest file
    filePath = path + '/' + allFiles[-1]
    xl = pd.read_excel(fileName, sheetname=None, index_col=0)

    




    # product string parsing from the correct data sheet