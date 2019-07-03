# Filling forms on Shaw's website

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to fill forms on Shaw website
def cartFormFilling(extensionPath, driverPath):

    """
       extensionPath: system path for unpacked Adobe extension
           (eg. '/Users/JohnDoe/Documents/data-bot/adobe-debugger')
       driverPath: system path for Chrome driver
           (eg. '/Users/JohnDoe/Documents/data-bot/chromedriver')
    """

    options = Options()

    options.add_argument('--load-extension={}'.format(extensionPath))
    driver = webdriver.Chrome(driverPath, options=options)

    #load desired webpage
    driver.get('https://test-ecommerce-discover-test-external.nonprod.dsl.aws.shaw.ca/')
    driver.get('https://test-ecommerce-discover-test-external.nonprod.dsl.aws.shaw.ca/bundles')
    driver.find_element_by_class_name('c-card__checkout-label').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "Yes")))
    driver.execute_script("document.getElementById('Yes').click()")
    driver.execute_script("document.getElementById('Internet').click()")
    driver.execute_script("document.getElementById('Television').click()")
    driver.execute_script("document.getElementById('Telephony').click()")
    driver.execute_script("document.querySelector('[aria-label=\"Submit your details\"]').click()")

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "address")))
    element.click()

    locationField = driver.find_element_by_id('address')
    locationField.send_keys('121 Copperfield Grove Southeast, Calgary, AB, Canada') # you can't click enter to confirm

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "ChIJXwsBHvF3cVMRpneKEZEV9SE"))) # this executes a script after, so no var
    driver.execute_script("document.getElementById('ChIJXwsBHvF3cVMRpneKEZEV9SE').click()")

    element = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.CLASS_NAME, "c-self-identify__validate-address-button")))
    element.click()
    # shift command backspace - clears cache

    goToCart = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "c-self-identify__serviceability-success-button")))
    goToCart.click()
    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "c-cart__checkout-btn")))
    proceed.click()

    # Shopping cart form
    # 1 Contact details
    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "firstName")))
    proceed.send_keys('test')
    driver.find_element_by_id('lastName').send_keys('test')
    driver.find_element_by_id('contactEmail').send_keys('test@test.com')
    driver.find_element_by_id('contactPhoneNumber').send_keys('416-645-1500')
    driver.execute_script("document.querySelector('[aria-label=\"Save Contact details and continue to Service address\"]').click()")

    # 2 Service address
    driver.execute_script("document.querySelector('[aria-label=\"Save Service address details and continue to Installation\"]').click()")

    # 3 Installation
    driver.find_element_by_id('installPreferenceType').click()

    # driver.find_element_by_id('0').click()
    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "0")))
    proceed.click()

    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "c-installation__save-and-continue")))
    proceed.click()

    # 4 Billing information
    driver.execute_script("document.querySelector('[aria-label=\"Save billing information and continue to summary\"]').click()")

    # 5 Value Plan agreement
    driver.execute_script("document.querySelector('[aria-label=\"Read and accept agreement this will be displayed in a dialog\"]').click()")
    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "c-fullwidth-button__icon--up")))
    proceed.click()

    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "accepted")))
    proceed.click()

    driver.find_element_by_id('signature').click()
    driver.find_element_by_id('signature').send_keys('test test')
    driver.execute_script("document.querySelector('[aria-label=\"Accept Agreement\"]').click()")
    proceed = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "is-active--submit")))
    proceed.click()


