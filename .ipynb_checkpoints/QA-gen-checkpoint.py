import os

repoPath = os.path.dirname(os.path.abspath(__file__))+'/chromedriver'
print(repoPath)


# Loads modified Adobe extension from directory and adds it to Selenium instance.
unpacked_extension_path = extensionPath
options = Options()

options.add_argument('--load-extension={}'.format(unpacked_extension_path))
driver = webdriver.Chrome(driverPath, options=options)