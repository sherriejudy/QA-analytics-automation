# Main script for page loads analytics

# Import required modules
import PageLoads
import Processing

websiteURL = 'https://test-ecommerce-discover-test-external.nonprod.dsl.aws.shaw.ca'
extensionPath = '/Users/rammangl1/Desktop/ShawWeb/shaw-data-bot/adobe-debugger'
driverPath = '/Users/rammangl1/Desktop/ShawWeb/shaw-data-bot/chromedriver'
userDir = '/Users/rammangl1'


PageLoads.endPointHits(websiteURL, userDir, extensionPath, driverPath)
Processing.CSV_prettifier(userDir + '/Downloads')




