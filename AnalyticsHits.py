# Navigating to all the page links and getting Adobe Analytics data

# Import required modules
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
import time
from pathlib import Path

# Function to download analytics data for all navigation links on the website
# Parses through the HTML navigation bar and uses the extension to download data
def endPointHits(websiteURL, userDir, extensionPath, driverPath):
    """
        websiteURL: URL for the page to be analysed
        userDir: system path for user's directory (eg. '/Users/JohnDoe')
        extensionPath: system path for unpacked Adobe extension
            (eg. '/Users/JohnDoe/Documents/data-bot/adobe-debugger')
        driverPath: system path for Chrome driver
            (eg. '/Users/JohnDoe/Documents/data-bot/chromedriver')
    """

    # Creating a Beautiful Soup Object with website's
    # Home page HTML
    try:
        response = get(websiteURL)
        htmlSoup = BeautifulSoup(response.text, 'html.parser')
    except:
        # Handling exception for wrong URL
        print('Exception: Not a valid URL')
        sys.exit(1)
    # print(html_soup.prettify())

    # Finding all navigation links for page load testing
    endPoints = []
    navLinks = htmlSoup.find('nav').find_all('a')

    for link in navLinks:
        # value of href attribute of each tag
        href = link.get('href')

        if href != None:
            # checking for full links vs end points
            if href.find('http') == -1:
                href = websiteURL + href
            # Standardizing URL
            if href[-1] == '/':
                href = href[:-1]
            if href.find('shaw') != -1:
                endPoints.append(href)

    # Remove duplicate links
    endPoints = list(dict.fromkeys(endPoints))

    # Handling no endpoints exception
    if not endPoints:
        print('Exception: No navigation endpoints found')
        sys.exit(1)

    # Exporting web endpoints to a CSV file
    with open(str(Path(userDir + '/Downloads/Endpoints.csv')), 'w') as f:
        # Joining links with newline delimiter to create rows
        f.write('\n'.join(endPoints))

    f.close()

    # Loads modified Adobe extension from directory and adds it to Selenium instance.
    unpacked_extension_path = extensionPath
    options = Options()

    options.add_argument('--load-extension={}'.format(unpacked_extension_path))
    driver = webdriver.Chrome(driverPath, options=options)

    # Downloading Page Load analytics for each page in CSV format
    for page in endPoints:
        driver.get(page)
        time.sleep(2)