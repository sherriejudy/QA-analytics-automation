# QA Analytics Automation

QA Analytics Automation gets Adobe Analytics data from Shaw.ca navigation bar links with a form filling feature, and a Graphical User Interface(GUI) for easy implementation. This bot parses the website's HTML code, gets the Adobe analytics data for all the navigation links and processes the data, providing an Excel sheet output of the processed information. Additional form filling for Shaw.ca is available through Selenium IDE. 

### Look how easy it is to use:

```
* Project setup
* Project run 
* Output Excel sheets
* Form filling
```

### Project Setup

* Repository: https://github.com/sherriejudy/QA-analytics-automation
* Clone the repository on your local machine
* Install Python 3
* Install Google Chrome (the browser used in the project)
* Command Line is used to set up and run the project
* Navigate to the project directory using Command Line
* Create a virtual environment in the project directory
  * Install virtualenv library:
    * `pip install virtualenv`
  * Create a virtual environment:
    * `virtualenv virtual-env-name`
  * Start virtual environment:
    * `source virtual-env-name/bin/activate`
  * Closing virtual environment (after your work is done):
    * `deactivate`
* Install Python dependencies
  * `pip install -r requirements.txt`

### Project Run

* Navigate to the project directory using Command Line
* Activate the virtual environment
  * `source virtual-env-name/bin/activate`
* Run the main Python script to access GUI
  * `pythonw Analytics.py`
* Graphical User Interface (GUI)
  * GUI (Analytics QA Bot) should pop up behind an empty chrome window - do not delete this chrome window!
  * On GUI, insert test site `https://www.shaw.ca` into Page Loads
    * click `start testing`
    * When testing is done, go into downloads
    * Open the Excel file containing all the Adobe Analytics data
    
### Project Output

The project opens a Chrome window and navigates to various links found on the provided website. The final output is an Excel sheet, containing the processed Adobe Analytics data with a processed product string, in the Downloads folder of the user. Navigate to the Excel sheet named summary in the very end, to find all page loads' in one Excel sheet. 

### Form filling option

Additional form filling is available with selenium IDE chrome extension. Two sample Shaw.ca form tests are already provided inside `ide_tests folder ` from your cloned repository. To run a test form: 

* Clear cache on your chrome browser
  * Go to Settings on chrome
  * Clear browsing data
* Using Selenium IDE
  * Install Selenium IDE from Google Chrome Extension store
  * Click on Selenium IDE icon on the extension bar
  * Open an existing project
    * Navigate to ide_tests folder from the cloned repository
    * Choose a file, open
  * Slow down Test execution speed slightly to prevent loading errors
  * Run current test
* Graphical User Interface (GUI)
  * Input xlsx file generated from form filling, this file should be located in the Downloads folder
  * Click `process form data`

### Creating a New Form
It is also easy to create a new form test with selenium IDE, simply choose the option to create a new project. General form structure on the Shaw.ca is customer/non-customer verification, with an option to check out shopping cart, as demonstrated by the sample Shaw.ca test forms for reference. 

### Built With

```
* Python
* Selenium Webdriver
* Pandas
* Beautiful Soup
* Adobe Experience Cloud Debugger
* Selenium IDE
```




