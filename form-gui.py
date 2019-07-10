import wx
import pandas as pd
import os
import time
import Processing as p
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pathlib import Path

class FormFill(wx.Frame):    
    def __init__(self):
        self.repoPath = os.path.dirname(os.path.abspath(__file__))
        super().__init__(parent=None, title='Form Filling Control Panel')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        
        my_btn = wx.Button(panel, label='Open WebDriver')
        my_btn.Bind(wx.EVT_BUTTON, self.seleniumIDE)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.EXPAND, 2)
        
        my_btn2 = wx.Button(panel, label='Close WebDriver')
        my_btn2.Bind(wx.EVT_BUTTON, self.seleniumIDE2)
        my_sizer.Add(my_btn2, 0, wx.ALL | wx.EXPAND, 2)
        
        self.text_ctrl = wx.TextCtrl(panel, value = 'Output File Name (.xlsx)')
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 2) 
        
        my_btn3 = wx.Button(panel, label='CSV Prettifier')
        my_btn3.Bind(wx.EVT_BUTTON, self.runCSV)
        my_sizer.Add(my_btn3, 0, wx.ALL | wx.EXPAND, 2)
        
        panel.SetSizer(my_sizer)        
        self.Show()
        
    
    def seleniumIDE(self, event):
            driverPath = str(Path(self.repoPath + '/chromedriver'))
            unpacked_extension_path = str(Path(self.repoPath + '/adobe-debugger'))
            unpacked_extension_path2 = str(Path(self.repoPath + '/seleniumIDE'))
            options = Options()

            options.add_argument('--load-extension={},{}'.format(unpacked_extension_path,unpacked_extension_path2))
            self.driver = webdriver.Chrome(driverPath, options=options)
    
    def seleniumIDE2(self, event):
        
        self.driver.quit()
    
    def runCSV (self, event):
        value = self.text_ctrl.GetValue()
        homeDir = os.path.expanduser('~')
        p.CSV_prettifier(str(Path(homeDir + '/Downloads')), 'endpoints.csv', value, forms = True)

if __name__ == '__main__':
    app = wx.App()
    frame = FormFill()
    app.MainLoop()