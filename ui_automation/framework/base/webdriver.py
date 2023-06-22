#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


"""
@package base

WebDriver class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriver(browser)
    wdf.getWebDriverInstance()
"""
import traceback
import os

from selenium import webdriver
from testSetup.dataSource.login import Login


class WebDriver():

    def __init__(self, browser):
        self.browser = browser
        self.config = Login()
        self.baseURL = self.config.baseURL

    def getDriverPath(self):
        fpath = os.path.abspath(__file__)
        while True:
              fpath, fname = os.path.split(fpath)
              if fname == 'zstest':
                 break
        for root, _, files in os.walk(fpath):
            for fname in files:
                if fname == "chromedriver":
                   return os.path.join(root, fname)

        return None


    def getWebDriverInstance(self):
        """
        Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        path = self.getDriverPath()

        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            driver = webdriver.Chrome(path)
        else:
            driver = webdriver.Chrome(path)

        # Maximize the window
        driver.maximize_window()

        # Loading browser with App URL
        driver.get(self.baseURL)
        return driver
