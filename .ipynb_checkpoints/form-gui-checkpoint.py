import wx
import pandas as pd
import os
import time
import Processing as p
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from pathlib import Path

class FormFill(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Form Filling Control Panel')
        panel = wx.Panel(self)        
        my_sizer = wx.BoxSizer(wx.VERTICAL) 
        
        wx.StaticText(panel, label="Testing")
        
        my_btn = wx.Button(panel, label='Selenium IDE Testing')
        my_btn.Bind(wx.EVT_BUTTON, self.seleniumIDE)
        my_sizer.Add(my_btn, 0, wx.ALL | wx.CENTER, 5)
        
        self.text_ctrl = wx.TextCtrl(panel, value = 'Output File Name (.xlsx)')
        my_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 5) 
        
        my_btn2 = wx.Button(panel, label='CSV Prettifier')
        my_btn2.Bind(wx.EVT_BUTTON, self.runCSV)
        my_sizer.Add(my_btn2, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(my_sizer)        
        self.Show()

    def seleniumIDE(self, event):
        value = self.text_ctrl.GetValue()
        if not value:
            print("You didn't enter anything!")
        else:
            print(f'You typed: "{value}"')
    
    def runCSV (self, event):
        p.CSV_prettifier()

if __name__ == '__main__':
    app = wx.App()
    frame = FormFill()
    app.MainLoop()