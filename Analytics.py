# Main script for page loads analytics

# Import required modules
import PageLoads
import Processing
import os
import sys
import platform

opSys = platform.system()

if opSys == 'Windows':
    slash = '\'
else:
    slash = '/'


print('Running on', opSys,'...')
# Home directory system path
homeDir = os.path.expanduser('~')
# System path to the cloned repository (eg. /Users/JohnDoe/Documents/shaw-data-bot)
repoPath = os.path.dirname(os.path.abspath(__file__))
# Website to be tested as a command line argument
websiteURL = sys.argv[1]

# Finding all navigation links and the associated analytics data
PageLoads.endPointHits(websiteURL, homeDir, repoPath + slash + 'adobe-debugger', repoPath + slash + 'chromedriver')
# Processing and collating analytics data
Processing.CSV_prettifier(homeDir + slash + 'Downloads')
