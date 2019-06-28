# Main script for Form analytics

# Import required modules
import Processing
import CartForm
import os
import sys
from pathlib import Path

print('Running...')
# Home directory system path
homeDir = os.path.expanduser('~')
# System path to the cloned repository (eg. /Users/JohnDoe/Documents/shaw-data-bot)
repoPath = os.path.dirname(os.path.abspath(__file__))
# Form to be tested as a command line argument
# formName = sys.argv[1]

# Filling form
CartForm.cartFormFilling(str(Path(repoPath + '/adobe-debugger')), str(Path(repoPath + '/chromedriver')))
# Processing and collating analytics data
Processing.CSVProcessing(str(Path(homeDir + '/Downloads')), 'FormFill-Endpoints.csv', 'FormFill-Analytics.xlsx', True)

print('Complete!')
