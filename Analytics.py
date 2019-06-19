# Main script for page loads analytics

# Import required modules
import PageLoads
import Processing

# Website to be tested
websiteURL = 'https://test-ecommerce-discover-test-external.nonprod.dsl.aws.shaw.ca'
# System path to the cloned repository (eg. /Users/JohnDoe/Documents/shaw-data-bot)
repoPath = '/Users/rammangl1/Desktop/ShawWeb/shaw-data-bot'
# System path to user directory (eg. /Users/JohnDoe)
userDir = '/Users/rammangl1'

# Finding all navigation links and the associated analytics data
PageLoads.endPointHits(websiteURL, userDir, repoPath + '/adobe-debugger', repoPath + '/chromedriver')
# Processing and collating analytics data
Processing.CSV_prettifier(userDir + '/Downloads')




