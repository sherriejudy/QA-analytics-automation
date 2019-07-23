# Navigating to all the page links and getting Adobe Analytics data

# Import required modules
import sys
import time
from pathlib import Path
from bs4 import BeautifulSoup
from requests import get

# Function to download analytics data for all navigation links on the website
# Parses through the HTML navigation bar and uses the extension to download data
def endPointHits(website_URL, user_dir, driver):
    """
        website_URL: URL for the page to be analysed
        user_dir: system path for user's directory (eg. '/Users/JohnDoe')
        driverPath: system path for Chrome driver
            (eg. '/Users/JohnDoe/Documents/data-bot/chromedriver')
    """

    # Creating a Beautiful Soup Object with website's
    # Home page HTML
    try:
        response = get(website_URL)
        html_soup = BeautifulSoup(response.text, 'html.parser')
    except:
        # Handling exception for wrong URL
        print('Exception: Not a valid URL')
        sys.exit(1)
    # print(html_soup.prettify())

    # Finding all navigation links for page load testing
    end_points = []
    nav_links = html_soup.find('nav').find_all('a')

    for link in nav_links:
        # value of href attribute of each tag
        href = link.get('href')

        if href != None:
            # checking for full links vs end points
            if href.find('http') == -1:
                href = website_URL + href
            # Standardizing URL
            if href[-1] == '/':
                href = href[:-1]
            if href.find(website_URL) != -1:
                end_points.append(href)

    # Remove duplicate links
    end_points = list(dict.fromkeys(end_points))

    # Handling no end_points exception
    if not end_points:
        print('Exception: No navigation end_points found')
        sys.exit(1)

    # Exporting web end_points to a CSV file
    with open(str(Path(user-dir + '/Downloads/end_points.csv')), 'w') as f:
        # Joining links with newline delimiter to create rows
        f.write('\n'.join(end_points))

    f.close()

    # Downloading Page Load analytics for each page in CSV format
    for page in end_points:
        driver.get(page)
        # Delay for proper data population
        time.sleep(3)
