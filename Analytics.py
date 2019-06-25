# Main script for page loads analytics

# Import required modules
import PageLoads
import DataProcessing
import os
import sys
import ProductString

from pathlib import Path

print('Running...')
# Home directory system path
homeDir = os.path.expanduser('~')
# System path to the cloned repository (eg. /Users/JohnDoe/Documents/shaw-data-bot)
repoPath = os.path.dirname(os.path.abspath(__file__))
# Website to be tested as a command line argument
websiteURL = sys.argv[1]

# Finding all navigation links and the associated analytics data
PageLoads.endPointHits(websiteURL, homeDir, str(Path(repoPath + '/adobe-debugger')), str(Path(repoPath + '/chromedriver')))
# Processing and collating analytics data
DataProcessing.CSVProcessing(str(Path(homeDir + '/Downloads')), 'Shaw-pageloads.xlsx', 'Endpoints-final.csv', False)

print('Complete.')
