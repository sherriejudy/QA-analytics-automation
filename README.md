### Shaw Analytics Bot

Parses the website's HTML code, gets the Adobe analytics data for all the navigation links and processes the data, providing an Excel sheet output of the processed information.

### Project Setup

* Clone the repository on your local machine
* Install Python 3
* Install Google Chrome (the browser used in the project)
* Command Line is used to setup and run the project
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
* Run the main Python script with the website URL as an argument
  * `python Analytics.py https://www.samplewebsite.com`
    
### Project Output

The project opens a Chrome window and navigates to various links found on the provided website. The final output is an Excel sheet, containing the processed Adobe Analytics data, in the Downloads folder of the user.





