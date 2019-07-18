# QA Analytics Automation

This tool is the perfect solution for pairing Adobe Analytics with your QA process. Using chromedriver, Selenium IDE and a simple but intuitive GUI, this tool can parse the target website's source code and return summary of all Adobe Analytics data from every page load. Additionally, utilizing selenium's IDE, the user can set up QA tests for future use and multiple testing sessions (i.e. form filling, navigation, etc.).

### Project Setup

* Clone the repository on your local machine.
* Install Python 3 (https://www.python.org/downloads/)
* Navigate to the project directory using Command Line.
* Create a virtual environment in the project directory:
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

### Project Run - Page Loads

* Navigate to the project directory using Command Line
* Activate the virtual environment
  * `source virtual-env-name/bin/activate`
* Run the main Python script to access GUI
  * `pythonw Analytics.py`
* Graphical User Interface (GUI)
  * GUI (Analytics QA Bot) should pop up behind an empty chrome window. **Note: do not close this chrome window!**
  * On GUI, insert test site url into the Page Loads text field
    * click `start testing`
    * When testing is done, go into downloads
    * Open the Excel file containing all the Adobe Analytics data
    
### Project Run - Form Filling

* Navigate to the project directory using Command Line
* Activate the virtual environment
  * `source virtual-env-name/bin/activate`
* Run the main Python script to access GUI
  * `pythonw Analytics.py`
* Graphical User Interface (GUI)
  * GUI (Analytics QA Bot) should pop up behind an empty chrome window. **Note: do not close this chrome window!**
  * On the empty Chrome window open the Selenium IDE extension where you will have the option to create a new test or open an old project and run the tests
    * Recording the test initially is a good start for setting up tests but fine tuning them and inserting steps that don't work manually ensures that Selenium can find all elements
    * Reducing test speed has been shown to produce better results with fewer errors
    * For more information on how to use Selenium IDE visit: (https://www.seleniumhq.org/selenium-ide/docs/en/introduction/getting-started/)
  * Once testing is complete input the desired output file name in Form Automation text field
    * click `process form data`
    * Open the downloads folder which will contain the output file that was previously specified along with a `product-strings.csv` file that contains all the product strings (if any) parsed in an easy to read format
    * Open the Excel file containing all the Adobe Analytics data
    
### Project Output

The project opens a Chrome window and navigates to various links found on the provided website. The final output is an Excel sheet, containing the processed Adobe Analytics data with a processed product string, in the Downloads folder of the user. Navigate to the Excel sheet named summary in the very end, to find all page loads' in one Excel sheet. 


### Built With

```
* JavaScript
* Python
* Pandas
* Selenium Webdriver
* Selenium IDE
* Beautiful Soup
* Adobe Analytics
```
