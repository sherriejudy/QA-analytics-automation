import wx
import os
import Processing
import sys
import AnalyticsHits
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class AnalyticsBot(wx.Frame):
    def __init__(self):
        # Path Initializations
        self.repoPath = os.path.dirname(os.path.abspath(__file__))
        self.homeDir = os.path.expanduser('~')

        # Driver and extension additions
        driverPath = str(Path(self.repoPath + '/chromedriver'))
        unpacked_extension_path = str(Path(self.repoPath + '/adobe-debugger'))
        unpacked_extension_path2 = str(Path(self.repoPath + '/seleniumIDE'))

        options = Options()
        options.add_argument('--load-extension={},{}'.format(unpacked_extension_path,unpacked_extension_path2))
        self.driver = webdriver.Chrome(driverPath, options=options)

        super().__init__(parent = None, title = 'Analytics QA Bot')
        # Creating a panel
        panel = wx.Panel(self)

        # Column layout
        column = wx.BoxSizer(wx.VERTICAL)
    
        # Text label
        lbl = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        lbl.SetLabel('Page Loads:')
        column.Add(lbl, 0, wx.ALIGN_LEFT)
    
        # Text entry field
        self.webURL = wx.TextCtrl(panel, value = 'https://www.test.com')
        column.Add(self.webURL, 0, wx.ALL | wx.EXPAND, 2)
        
        # Page loads testing button
        my_btn1 = wx.Button(panel, label='Start Testing')
        my_btn1.Bind(wx.EVT_BUTTON, self.pageLoads)
        column.Add(my_btn1, 0, wx.ALL | wx.EXPAND, 2)

        # Text label
        lbl = wx.StaticText(panel, -1, style=wx.ALIGN_CENTER)
        lbl.SetLabel('Form Automation:')
        column.Add(lbl, 0, wx.ALIGN_LEFT)

        # Text entry field
        self.formOutput = wx.TextCtrl(panel, value='Output.xlsx')
        column.Add(self.formOutput, 0, wx.ALL | wx.EXPAND, 2)

        # Page loads testing button
        my_btn2 = wx.Button(panel, label='Process Form Data')
        my_btn2.Bind(wx.EVT_BUTTON, self.formAutomation)
        column.Add(my_btn2, 0, wx.ALL | wx.EXPAND, 2)

        # Set panel size
        panel.SetSizer(column)
        wx.Window.SetSize(panel, width = 300, height = 400)

        # Show the frame window
        self.Show()

    def pageLoads(self, event):
        # Hide frame window
        self.Hide()
        
        # Finding all navigation links and the associated analytics data
        AnalyticsHits.endPointHits(self.webURL.GetValue(), self.homeDir, self.driver)
        #  Close driver window
        self.driver.quit()

        print('Downloaded Analytics Data')
        print('Processing...')

        # Processing and collating analytics data
        Processing.CSV_prettifier(str(Path(self.homeDir + '/Downloads')), 'Endpoints.csv', 'Pageloads.xlsx', False)

        print('\nComplete!')

        sys.exit()

    
    def formAutomation(self, event):
        #  Hide frame window
        self.Hide()
        #  Close driver window
        self.driver.quit()

        print('Completed Selenium Form Tests')
        print('Processing...')

        # Processing and collating analytics data
        Processing.CSV_prettifier(str(Path(self.homeDir + '/Downloads')), '', self.formOutput.GetValue(), True)

        print('\nComplete')

        sys.exit()


if __name__ == '__main__':
    app = wx.App()
    frame = AnalyticsBot()
    app.MainLoop()